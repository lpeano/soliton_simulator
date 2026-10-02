# -*- coding: utf-8 -*-
"""**LA TERZA VIA per le derivate sporche: il VELENO. Misurata, non supposta.**

**Mandato del guardiano, 2026-10-01.** L'opzione *«ai confini»* **non funziona**: dopo `mitosi` una
derivata e' sporca **legittimamente** fino alla voce che la riscrive, quindi un controllo al confine
### **o la segnala per sbaglio o non controlla nessuna lettura.**

**La terza via proposta:** alla nascita le derivate dei nuovi nodi si riempiono con un valore
**AVVELENATO** *(`NaN` per i float)*, e il controllo unico verifica che ### **nessuna grandezza di
STATO contenga valori non finiti**. Una lettura sporca ### **propaga il veleno nello stato** e viene
presa **al confine successivo**.

## Che cosa questa sonda misura, e sono le tre cose che il mandato chiede

| | |
|---|---|
| **1** | ### **il COSTO del controllo di finitezza per passo**, alle dimensioni VERE della scena grande, e **in rapporto al costo di un passo** |
| **2** | ### **le derivate INTERE**: quante sono, e che cosa si fa dove `NaN` non esiste |
| **3** | ### **l'interazione con `np.seterr(invalid='raise')`** *(`:8835`)*: un `NaN` che entra in un'operazione **solleva** o **propaga**? |

### ⚠ **E una QUARTA cosa, che non era nel mandato e cambia la proposta**
Il censimento dei **non finiti su un run SANO**: se una grandezza di **STATO** contiene **gia'**
valori non finiti **per disegno**, ### **un controllo globale di finitezza spara al primo passo** —
e allora il veleno **non si distingue** da cio' che e' legittimo.

COMANDO:  python csv/_test_fork/_sonda_veleno.py [--passi=3]
USCITA:   0 sempre: e' una SONDA per il piano, non un sigillo.
"""
import contextlib
import io
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sonda_veleno")


def carica(passi):
    """Scena **GRANDE**, `nmasse` e `sep` **da `a`**, come fa il pilota."""
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_veleno")
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
        net = S.net
        t0 = time.perf_counter()
        for _ in range(passi):
            _passo.passo_pieno(S, net)
        dt = (time.perf_counter() - t0) / max(passi, 1)
    return S, net, dt


def controllo_finitezza(net, voci):
    """Il controllo proposto: **nessuna grandezza di STATO con valori non finiti.**"""
    sporche = []
    with np.errstate(all="ignore"):
        for nome, _forma, tipo in voci:
            v = getattr(net, nome, None)
            if v is None:
                continue
            arr = v if isinstance(v, np.ndarray) else None
            if arr is None or arr.dtype.kind not in "fc":
                continue
            if not np.all(np.isfinite(arr)):
                sporche.append(nome)
    return sporche


def principale():
    passi = 3
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    S, net, dt_passo = carica(passi)
    n, m = int(net.n), int(len(net.i))
    print("scena GRANDE: n = %d, archi = %d, dopo %d passi" % (n, m, passi))
    print("costo di UN PASSO, misurato: %.3f s" % dt_passo)
    print("")

    # ---------------------------------------------------------------- 4: il CENSIMENTO
    print("=" * 100)
    print("4. I NON FINITI SU UN RUN SANO -- e non era nel mandato")
    print("=" * 100)
    trovati = []
    with np.errstate(all="ignore"):
        for nome, _f, tipo in S.REGISTRO_STATO:
            v = getattr(net, nome, None)
            if not isinstance(v, np.ndarray) or v.dtype.kind not in "fc":
                continue
            q_inf = int(np.sum(np.isinf(v)))
            q_nan = int(np.sum(np.isnan(v)))
            if q_inf or q_nan:
                trovati.append((nome, tipo, q_inf, q_nan, int(v.size)))
    print("  grandezze di STATO con valori NON FINITI: %d" % len(trovati))
    for nome, tipo, qi, qn, tot in trovati:
        print("    %-14s %-11s inf %-7d nan %-7d su %d" % (nome, tipo, qi, qn, tot))
    if trovati:
        print("  ### UN CONTROLLO GLOBALE DI FINITEZZA SPARA SUBITO: il veleno NON si distingue")
        print("      da cio' che e' legittimo, e la proposta va RAFFINATA.")
    else:
        print("  ### nessuna: un controllo globale di finitezza sarebbe PULITO.")
    print("")

    # ---------------------------------------------------------------- 1: il COSTO
    print("=" * 100)
    print("1. IL COSTO del controllo di finitezza, alle dimensioni VERE")
    print("=" * 100)
    for giro in range(2):                      # il primo giro scalda le cache
        t0 = time.perf_counter()
        for _ in range(10):
            controllo_finitezza(net, S.REGISTRO_STATO)
        dt = (time.perf_counter() - t0) / 10.0
    print("  un controllo su tutte le %d voci di STATO: %.6f s" % (len(S.REGISTRO_STATO), dt))
    print("  un PASSO: %.3f s" % dt_passo)
    print("  ### il controllo costa il %.3f %% di un passo" % (100.0 * dt / max(dt_passo, 1e-12)))
    print("  e con 9 controlli per passo (la generalizzazione 2): %.3f %%"
          % (100.0 * 9 * dt / max(dt_passo, 1e-12)))
    print("")

    # ---------------------------------------------------------------- 2: le DERIVATE INTERE
    print("=" * 100)
    print("2. LE DERIVATE INTERE: dove `NaN` NON ESISTE")
    print("=" * 100)
    import re
    tipi = {}
    for r in io.open(os.path.join(RADICE, "doc", "REGISTRO_grandezze.md"), encoding="utf-8"):
        mm = re.match(r"^\|\s*`([A-Za-z_][A-Za-z0-9_]*)`\s*\|\s*`([0-9×]+)`\s*\|\s*`([^`]*)`", r)
        if mm:
            tipi[mm.group(1)] = mm.group(3)
    interi, float_, altre = [], [], []
    # ### QUATTRO campi dal `COMMIT 4`: il registro dichiara anche la CLASSE DI
    #   NASCITA (`avvelena` / `auto-rinfresco`), e un unpack a tre si romperebbe.
    for nome, _dove, _classe_nascita, _motivo in S.REGISTRO_DERIVATE:
        t = tipi.get(nome, "(non misurato)")
        (interi if t.startswith("int") else float_ if t.startswith(("float", "complex"))
         else altre).append((nome, t))
    print("  derivate totali: %d" % len(S.REGISTRO_DERIVATE))
    print("  float/complex (il veleno `NaN` ESISTE): %d  %s"
          % (len(float_), [x[0] for x in float_]))
    print("  ### INTERE (il veleno NaN NON esiste): %d  %s" % (len(interi), interi))
    if altre:
        print("  altre: %s" % altre)
    print("")

    # ---------------------------------------------------------------- 3: `seterr`
    print("=" * 100)
    print("3. L'INTERAZIONE con `np.seterr(invalid='raise')` -- misurata, non supposta")
    print("=" * 100)
    vecchio = np.seterr(over="raise", divide="raise", invalid="raise", under="ignore")
    prove = (
        ("assegnare NaN in un array", lambda: np.array([1.0, np.nan])),
        ("SOMMA con NaN", lambda: np.array([1.0, np.nan]) + 1.0),
        ("PRODOTTO con NaN", lambda: np.array([1.0, np.nan]) * 2.0),
        ("CONFRONTO > con NaN", lambda: np.array([1.0, np.nan]) > 0.5),
        ("np.isfinite su NaN", lambda: np.isfinite(np.array([1.0, np.nan]))),
        ("np.sum con NaN", lambda: float(np.sum(np.array([1.0, np.nan])))),
        ("astype(int64) su NaN", lambda: np.array([1.0, np.nan]).astype(np.int64)),
        ("inf - inf", lambda: np.array([np.inf]) - np.array([np.inf])),
    )
    for etichetta, f in prove:
        try:
            f()
            print("  %-26s -> PASSA (il NaN PROPAGA, nessuna eccezione)" % etichetta)
        except FloatingPointError as e:
            print("  %-26s -> ### SOLLEVA FloatingPointError: %s" % (etichetta, str(e)[:44]))
        except Exception as e:
            print("  %-26s -> altro: %s" % (etichetta, type(e).__name__))
    np.seterr(**vecchio)
    print("")
    print("### LA LETTURA SI DERIVA DAI RISULTATI QUI SOPRA, e sta nel piano: il veleno e' utile")
    print("    SOLO SE PROPAGA. Dove solleva, il difetto si vede subito ma con un'eccezione NON")
    print("    DICHIARATA; dove propaga, lo prende il controllo al confine -- se il controllo lo")
    print("    sa distinguere da cio' che e' legittimo.")
    return 0


if __name__ == "__main__":
    sys.exit(principale())
