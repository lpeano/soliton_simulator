# -*- coding: utf-8 -*-
"""IL COLLAUDO DEL BANCO — **e il BRACCIO `0` e' una SIMMETRIA, non un numero.**

> ## ⛔ **IL BRACCIO `0`, che il mandato chiede PRIMA DI TUTTO IL RESTO:** definire
> ## l'operatore di **coniugazione di carica** e **PROVARE che la camminata lineare e'
> ## simmetrica** sotto di lui. ### **Se non lo e', si FERMA e si scrive.**

**Le soglie sono quelle del task history**, e sono **derivate**:

| | la soglia | la forma |
|---|---|---|
| `S1` | isotropia | `T · g_max · ε · ‖ψ‖` — **un conteggio di operazioni** |
| `S2` | cono | ### **`0.0` al bit** |
| `S3` | norma | `passi · n_estremita · ε` |
| `S6` | coniugazione | ### **`0.0` al bit** |

### ⚠ **E OGNI BRACCIO CHE DICE <<PASSA>> HA MATERIA**, perche' un confronto su un insieme
vuoto **passa sempre**: i gradi sono **davvero diversi**, i nodi oltre il cono **esistono**,
e la rottura di `(A)` e' **davvero diversa da zero**.

Gira con:  python proto_camminata/_collauda_banco.py
"""
import hashlib
import io
import math
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                               # noqa: E402

_presidio.avvia(__file__)

import camminata as CM                                         # noqa: E402
import nonlineare as NL                                        # noqa: E402
import scena as SC                                             # noqa: E402

EPS = float(np.finfo(float).eps)
NLN = chr(10)
SEME = 11
PASSI = 60

# ### ⛔ **I FILE DEL BANCO, dichiarati:** servono ai due bracci che guardano
# ### ### **il SORGENTE** *(niente simulatore, niente clip)*.
MIEI = ("scena.py", "camminata.py", "nonlineare.py", "_collauda_banco.py",
        "_letture.py", "_referto.py")
# ### ⛔ **I FILE DI FISICA DEL BANCO, cioe- MIEI MENO QUESTO** -- e la ragione e-
# ### precisa: ### **questo file NOMINA le forme di un clip per cercarle**, quindi
# ### ### **non puo- essere il soggetto della propria ricerca.**
# ### ⚠ **Trovato dal braccio stesso al primo giro**, che e- il modo giusto di
# ### scoprirlo: ### **un braccio che accusa se stesso e- un braccio mal definito.**
FISICA = ("scena.py", "camminata.py", "nonlineare.py", "_letture.py")
# ### ⚠ **LE FORME DI UN CLIP**, dichiarate una a una. ### **`min(u, v)` NON e- un
# ### clip**: ordina i due estremi di un arco, e il braccio non lo confonde perche-
# ### ### **cerca le forme che agiscono su un ARRAY.**
CLIP = ("np.clip", ".clip(", "np.maximum", "np.minimum", "np.fmax", "np.fmin")


def main():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DEL BANCO DELLA CAMMINATA")
    print("=" * 100)
    SC._niente_simulatore()

    sc = SC.irregolare()
    reg = SC.regolare()
    r = SC.ritmi(sc, SEME)
    psi = CM.stato_casuale(sc, SEME)
    gmax = int(sc["grado"].max())
    nest = 2 * sc["m"]

    # ================================================================ MATERIA
    gradi = sorted(set(sc["grado"].tolist()))
    esito("### MATERIA: il grafo e- DAVVERO irregolare", len(gradi) >= 3,
          "### %d gradi distinti: %s -- su un grafo regolare l-isotropia non direbbe niente"
          % (len(gradi), gradi))
    d0 = SC.distanze(sc, 0)
    esito("### MATERIA: il grafo e- CONNESSO", int(d0.min()) >= 0,
          "### eccentricita- dal nodo 0: %d archi" % int(d0.max()))

    # ================================================================ IL BANCO E- UN BANCO
    testi = {}
    for nome in MIEI:
        p = os.path.join(_QUI, nome)
        testi[nome] = io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    # ### ⛔ **SI CERCA UN IMPORT, NON UNA PAROLA** -- e la differenza l-ha trovata
    # ### il braccio al primo giro: ### **`scena.py` e questo file NOMINANO il simulatore**,
    # ### il primo nella funzione che lo VIETA e il secondo nel controllo stesso.
    # ### ✅ **Cio- che conta e- se lo IMPORTA**, e un import ha due forme sole.
    # ### ⚠ **E ANCHE QUI SOLO I FILE DI FISICA, per la STESSA ragione un livello
    # ### piu- sotto:** questo file ### **nomina le due forme di un import** per cercarle,
    # ### quindi ### **accuserebbe se stesso.** ### ✅ **E a questo file ci pensa
    # ### `_niente_simulatore()` A RUNTIME**, che per un file CHE GIRA e- piu- forte di una
    # ### ricerca nel testo: ### **guarda `sys.modules`, cioe- cio- che e- DAVVERO
    # ### importato**, import indiretti compresi.
    cattivi = [n for n, t in testi.items() if n in FISICA
               and ("import soliton_simulator" in t or "from soliton_simulator" in t)]
    esito("### il banco non IMPORTA il simulatore, nel SORGENTE", not cattivi,
          "### cercate le due forme di un import; e `_niente_simulatore()` guarda "
          "`sys.modules`: %s" % (cattivi or "nessuno dei %d file" % len(testi)))
    trovati = [(n, c) for n, t in testi.items() if n in FISICA for c in CLIP if c in t]
    esito("### NESSUN clip, pavimento o tetto nei file di FISICA del banco", not trovati,
          "### %d forme cercate in %d file: un clip violerebbe `A14` per costruzione%s"
          % (len(CLIP), len(FISICA),
             ("; TROVATI: %s" % trovati) if trovati else ""))

    # ### ⛔ **E IL BANCO NON ENTRA NELLA TABELLA DELLE LEGGI**, che e- la terza
    # ### cosa che il mandato pretende *(<<NON entra in `leggi.yaml`>>)*: si verifica
    # ### ### **leggendo la tabella**, non promettendolo.
    _leggi = os.path.join(RADICE, "primo_ordine", "leggi", "leggi.yaml")
    _t = io.open(_leggi, encoding="utf-8").read() if os.path.exists(_leggi) else ""
    esito("### il banco NON entra in `leggi.yaml`",
          "camminata" not in _t and "proto_camminata" not in _t,
          "### la tabella delle leggi non lo nomina: un banco NON E- UNA LEGGE")

    # ================================================================ IL BRACCIO 0
    a = CM.coniuga(CM.passo(psi, sc, r, 1.0))
    b = CM.passo(CM.coniuga(psi), sc, r, 1.0)
    dif = float(np.max(np.abs(a - b)))
    esito("### BRACCIO 0: la camminata LINEARE e- simmetrica sotto `C`, AL BIT", dif == 0.0,
          "### max|C(U psi) - U(C psi)| = %.3g -- e la derivazione diceva ESATTAMENTE 0"
          % dif)
    cc = float(np.max(np.abs(CM.coniuga(CM.coniuga(psi)) - psi)))
    esito("### e `C` e- una INVOLUZIONE: `C(C psi) = psi` al bit", cc == 0.0,
          "### max|C(C psi) - psi| = %.3g" % cc)

    # ================================================================ LE DUE NON LINEARI
    for nome, f, _nota in NL.LE_DUE:
        a = CM.coniuga(CM.passo(psi, sc, r, 1.0, 1.0, f))
        b = CM.passo(CM.coniuga(psi), sc, r, 1.0, 1.0, f)
        d = float(np.max(np.abs(a - b)))
        if nome == "A":
            esito("### DEVE ROMPERE `C`: la fase PARI (A)", d > 0.0,
                  "### max|C(U psi) - U(C psi)| = %.3g -- e- IL BRACCIO CHE DEVE FALLIRE "
                  "la lettura 5" % d)
        else:
            esito("### NON deve rompere `C`: la fase DISPARI (B), AL BIT", d == 0.0,
                  "### max|C(U psi) - U(C psi)| = %.3g" % d)

    # ================================================================ LA NORMA (S3)
    tolN = PASSI * nest * EPS
    for nome, f in (("lineare", None), ("(A)", NL.fase_pari), ("(B)", NL.fase_dispari)):
        fine, _ = CM.corri(psi, sc, r, 1.0, PASSI, 1.0 if f else 0.0, f)
        sc_n = abs(CM.norma(fine) - CM.norma(psi))
        esito("la NORMA si conserva entro `passi*n_est*eps` -- %s" % nome, sc_n <= tolN,
              "### scarto %.3g, soglia %.3g (= %d * %d * eps)"
              % (sc_n, tolN, PASSI, nest))

    # ================================================================ IL CONO (S2)
    # ### ⛔ **IL `T` DEL CONO ESCE DA UNA MISURA, non da un gusto:** meta-
    # ### dell-eccentricita-, cosi- ### **i nodi oltre il cono ESISTONO SEMPRE** -- e su
    # ### questo grafo l-eccentricita- e- 6, quindi `T=60` sarebbe un braccio VUOTO.
    T = max(1, int(d0.max()) // 2)
    oltre = int(np.sum(d0 > T))
    esito("### MATERIA del cono: ci sono nodi OLTRE %d archi" % T, oltre > 0,
          "### %d nodi oltre il cono -- con T=%d (meta- dell-eccentricita- %d) il braccio "
          "ha materia" % (oltre, T, int(d0.max())))
    base, _ = CM.corri(CM.stato_zero(sc) + 0.0, sc, r, 1.0, 0)
    uno = CM.stato_zero(sc)
    # una sola estremita- del nodo 0, ampiezza 1 nella banda +
    e0 = int(np.nonzero(sc["nodo"] == 0)[0][0])
    uno[e0, 0] = 1.0
    due = uno.copy()
    due[e0, 0] = 1.0 + 1e-3
    f1, _ = CM.corri(uno, sc, r, 1.0, T)
    f2, _ = CM.corri(due, sc, r, 1.0, T)
    diff = np.abs(f1 - f2).sum(axis=1)
    fuori = diff[d0[sc["nodo"]] > T]
    esito("### IL CONO: oltre %d archi la differenza e- ZERO ESATTO" % T,
          float(np.max(fuori)) == 0.0 if fuori.size else False,
          "### max|differenza| fuori dal cono = %.3g su %d estremita-"
          % (float(np.max(fuori)) if fuori.size else -1, int(fuori.size)))

    # ================================================================ L'ISOTROPIA (S1)
    nuova, pn, mappa = SC.rinumera(sc, 23)
    rn = np.empty_like(r)
    rn[pn] = r
    for esatta in (True, False):
        f1, _ = CM.corri(psi, sc, r, 1.0, PASSI, esatta=esatta)
        pn_psi = np.zeros_like(psi)
        pn_psi[mappa] = psi
        f2, _ = CM.corri(pn_psi, nuova, rn, 1.0, PASSI, esatta=esatta)
        rip = np.zeros_like(f2)
        rip[mappa] = f1
        d = float(np.max(np.abs(rip - f2)))
        tol = PASSI * gmax * EPS * math.sqrt(CM.norma(psi))
        if esatta:
            esito("### ISOTROPIA con somma ESATTA (`fsum`): ZERO AL BIT", d == 0.0,
                  "### max|differenza| = %.3g -- in aritmetica esatta l-isotropia e- ESATTA"
                  % d)
        else:
            esito("ISOTROPIA con la somma di `numpy`: entro `T*g_max*eps`", d <= tol,
                  "### max|differenza| = %.3g, soglia %.3g (= %d * %d * eps)"
                  % (d, tol, PASSI, gmax))

    # ================================================================ LA LETTURA 6
    uni = np.ones(sc["n"], dtype=float)
    f1, _ = CM.corri(psi, sc, uni, 1.0, PASSI)
    f2 = psi.copy()
    for _ in range(PASSI):
        f2 = CM.passo_dt_globale(f2, sc, 1.0)
    d = float(np.max(np.abs(f1 - f2)))
    esito("### LETTURA 6: con `r=1` coincide col `dt` GLOBALE, AL BIT", d == 0.0,
          "### max|differenza| = %.3g, e sono DUE STRADE di codice diverse" % d)

    # ================================================================ IL CONTROLLO REGOLARE
    rr = SC.ritmi(reg, SEME)
    pr = CM.stato_casuale(reg, SEME)
    fine, _ = CM.corri(pr, reg, rr, 1.0, PASSI)
    esito("il CONTROLLO regolare gira e conserva la norma",
          abs(CM.norma(fine) - CM.norma(pr)) <= PASSI * 2 * reg["m"] * EPS,
          "### scarto %.3g sul 4-regolare" % abs(CM.norma(fine) - CM.norma(pr)))

    # ================================================================ IL DETERMINISMO
    imp = []
    for _ in range(2):
        p = subprocess.run([sys.executable,
                            os.path.join(_QUI, "camminata.py"), "--impronta"],
                           cwd=RADICE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        for riga in (p.stdout or "").split(NLN):
            if "IMPRONTA" in riga:
                imp.append(riga.split()[-1])
    esito("### il DETERMINISMO fra DUE PROCESSI: byte identici",
          len(imp) == 2 and imp[0] == imp[1],
          "### %s" % (imp[0][:16] if imp else "nessuna impronta"))

    print("=" * 100)
    print("IL COLLAUDO DEL BANCO: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
