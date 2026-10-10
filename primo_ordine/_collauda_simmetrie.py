# -*- coding: utf-8 -*-
"""IL COLLAUDO DI `P-SIM` — **le simmetrie SIMBOLICHE e le conservazioni NUMERICHE.**

### ⭐ **E LE DUE META' SONO DUE COSE DIVERSE, non due modi di dire la stessa.** La
simmetria si verifica ### **in sympy**, su un'espressione, e il verdetto è
### **esatto: zero o non zero.** La conservazione si verifica ### **su una corsa**, e il
verdetto è ### **un numero contro una soglia** — e ### ⛔ **la soglia è il punto in cui un
collaudo del genere diventa una manopola.**

### ✅ **LE DUE SOGLIE SONO DERIVATE DALL'ORDINE DEL METODO, e nessuna è stata tarata:**
`NORMA` → `passi * eps` *(invariante quadratico: solo arrotondamento)*, `ENERGIA` →
`dt^2` *(metodo simmetrico del secondo ordine, senza deriva secolare)*. ### **La
derivazione sta nel docstring di `simmetrie.py`.**

### ⚠ **E SONO UNDICI ORDINI DI GRANDEZZA DI DIFFERENZA**, che dice una cosa vera: ###
**la norma è conservata DALLA STRUTTURA del metodo, l'energia solo APPROSSIMATA.**
### ⛔ **Dichiararle con la stessa soglia nasconderebbe esattamente questo.**

### ⛔ **E CIO' CHE QUESTO COLLAUDO NON DICE: le tre leggi sono di PROVA.** Una simmetria
verificata su `PROVA-HOPPING` ### **non dice niente sulla fisica** — dice che
### **la macchina funziona.**
"""
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "config"))
sys.path.insert(0, os.path.join(_QUI, "leggi"))

import driver as DRV                                        # noqa: E402
import hamiltoniana as HAM                                   # noqa: E402
import passo as PA                                           # noqa: E402
import schema_config as CFG                                  # noqa: E402
import simmetrie as SM                                       # noqa: E402
import stato as ST                                           # noqa: E402

NL = chr(10)
CONFIG = os.path.join(_QUI, "config", "prova.yaml")


def _tabella():
    import yaml
    with io.open(os.path.join(_QUI, "leggi", "leggi.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DI `P-SIM` -- SIMMETRIE (simboliche) e CONSERVAZIONI (numeriche)")
    print("=" * 100)
    tab = _tabella()
    leggi = tab["leggi"]
    print("  le leggi in tabella: %d" % len(leggi))
    for lg in leggi:
        print("     %-16s simmetrie %-42s conserva %s"
              % (lg["id"], lg.get("simmetrie"), lg.get("conserva")))
    print()
    # ============================================================ (a) LE SIMMETRIE
    esito("### il collaudo ha MATERIA: ogni legge dichiara delle simmetrie",
          all(lg.get("simmetrie") for lg in leggi),
          "%d leggi: ### senza dichiarazioni non ci sarebbe niente da verificare"
          % len(leggi))
    esito("NON deve scattare: le simmetrie DICHIARATE sono VERE",
          SM.controlla(leggi) == [],
          "### verificate SIMBOLICAMENTE: la differenza deve essere ZERO in sympy, non "
          "<<piccola>>")
    # ### ⛔ **IL CASO CHE DEVE FALLIRE SI COSTRUISCE DALLA LEGGE VERA**, in memoria:
    # ### si toglie ### **un solo coniugato** da `PROVA-LOCALE`, e la fase ### **non si
    # ### cancella piu-.**
    loc = next(lg for lg in leggi if lg["id"] == "PROVA-LOCALE")
    rotta = dict(loc, id="PROVA-ROTTA",
                 espressione=str(loc["espressione"]).replace("psi_0c", "psi_0", 1))
    e = SM.rompe(rotta)
    esito("### DEVE scattare: una legge che ROMPE la `U(1)` dichiarata",
          any("NON LA RISPETTA" in x for x in e),
          "### togliere UN coniugato: la fase non si cancella piu-, e sympy lo vede "
          "ESATTAMENTE")
    esito("### DEVE scattare: `SCAMBIO-DEI-CAPI` su un termine di NODO",
          any("NON HA DUE CAPI" in x for x in SM.rompe(
              dict(loc, simmetrie=["U1-FASE-GLOBALE", "SCAMBIO-DEI-CAPI"]))),
          "### e- il FALSO-UNO: la sostituzione non tocca nessun simbolo, quindi "
          "<<sembra verificato>> senza aver guardato niente")
    esito("NON deve scattare: zero sostituzioni di `U(1)` su una legge SENZA `psi`",
          SM.rompe({"id": "PROVA-RHO", "tipo": "termine_nodo", "espressione": "rho**2",
                    "simmetrie": ["U1-FASE-GLOBALE"], "conserva": []}) == [],
          "### e- INVARIANTE DAVVERO, non per vacuita-: la legge NON COINVOLGE LA FASE "
          "-- ed e- la distinzione che il collaudo dello schema mi ha insegnato")
    esito("### DEVE scattare: una legge che NON dichiara le simmetrie",
          any("NON DICHIARA" in x for x in SM.rompe(
              {k: v for k, v in loc.items() if k != "simmetrie"})),
          "### una simmetria non dichiarata e- una simmetria CHE NESSUNO VERIFICA")
    esito("### DEVE scattare: una simmetria FUORI VOCABOLARIO",
          any("CHIUSO" in x for x in SM.rompe(dict(loc, simmetrie=["PIPPO"]))),
          "### una simmetria nuova si dichiara CON IL SUO CONTROLLO, e una senza "
          "controllo e- UNA FRASE")
    esito("### DEVE scattare: `conserva` che NON e- una lista",
          any("LISTA" in x for x in SM.conservazioni_valide(dict(loc, conserva="NORMA"))),
          "### <<non dichiarato>> e <<non conserva niente>> non sono la stessa cosa")

    # ======================================================= (b) LE CONSERVAZIONI
    print()
    print("-" * 100)
    print("LE CONSERVAZIONI, MISURATE SU UNA CORSA -- contro soglie DERIVATE")
    print("-" * 100)
    c = CFG.carica(CONFIG)
    T = DRV.termini_attivi(c)
    ii, jj = DRV.grafo(c["scena"], c["nodi"])
    strati = PA.strati(ii, jj)
    st = ST.nuovo(c["nodi"])
    rng = np.random.default_rng(c["seme"])
    for k in st:
        st[k][...] = (rng.normal(size=st[k].shape) + 1j * rng.normal(size=st[k].shape))
    norma0 = float(np.sum(np.abs(st["psi"]) ** 2))
    e0 = float(HAM.energia(st, ii, jj, T))
    for _ in range(c["passi"]):
        st = PA.passo_locale(st, ii, jj, c["dt"], T, c["iterazioni"], c["toll"],
                             strati)[0]
    norma1 = float(np.sum(np.abs(st["psi"]) ** 2))
    e1 = float(HAM.energia(st, ii, jj, T))
    d_norma = abs(norma1 - norma0) / abs(norma0)
    d_ener = abs(e1 - e0) / abs(e0)
    s_norma = SM.soglia("NORMA", c["passi"], c["dt"])
    s_ener = SM.soglia("ENERGIA", c["passi"], c["dt"])
    print("  %d passi, dt = %g, integratore LOCALE, %d nodi"
          % (c["passi"], c["dt"], c["nodi"]))
    print("  NORMA    %.6f -> %.6f   deriva relativa %.3e   soglia %.3e (passi x eps)"
          % (norma0, norma1, d_norma, s_norma))
    print("  ENERGIA  %+.6f -> %+.6f   deriva relativa %.3e   soglia %.3e (dt^2)"
          % (e0, e1, d_ener, s_ener))
    esito("NON deve scattare: la `NORMA` sta sotto `passi * eps`",
          d_norma < s_norma,
          "%.3e < %.3e: ### la norma e- un INVARIANTE QUADRATICO, e il punto medio "
          "implicito li conserva ESATTAMENTE in aritmetica esatta -- quindi l-unico "
          "errore e- l-ARROTONDAMENTO" % (d_norma, s_norma))
    esito("NON deve scattare: l-`ENERGIA` sta sotto `dt^2`",
          d_ener < s_ener,
          "%.3e < %.3e: ### un metodo SIMMETRICO non ha deriva secolare dell-energia, e "
          "l-errore resta di ordine `dt^2`" % (d_ener, s_ener))
    esito("### e le DUE SOGLIE sono lontane di ORDINI DI GRANDEZZA",
          s_ener / s_norma > 1e8,
          "%.0e volte: ### e- la cosa VERA che le due soglie dicono -- la norma e- "
          "conservata DALLA STRUTTURA, l-energia solo APPROSSIMATA. Una soglia unica "
          "nasconderebbe esattamente questo" % (s_ener / s_norma))
    # ### ⛔ **E IL BRACCIO CHE DICE CHE LE SOGLIE NON SONO MANOPOLE:** si cambia
    # ### `dt` e ### **la soglia dell-energia cambia col QUADRATO.**
    esito("### e la soglia e- una FORMULA, non un numero: `dt/2` -> soglia `/4`",
          abs(SM.soglia("ENERGIA", c["passi"], c["dt"] / 2)
              - s_ener / 4) < 1e-30,
          "### un numero scritto a mano NON si muoverebbe con `dt`, e sarebbe una "
          "manopola (`A1`)")
    esito("### e la soglia della norma cresce col NUMERO DI PASSI",
          SM.soglia("NORMA", 2 * c["passi"], c["dt"]) == 2 * s_norma,
          "### perche- l-arrotondamento si ACCUMULA: e- la derivazione, non una scelta")

    print("=" * 100)
    print("IL COLLAUDO DI `P-SIM`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(collaudo())
