# -*- coding: utf-8 -*-
"""IL DRIVER — **la riga di comando sceglie SOLO IL FILE** *(punto `15(a)`)*.

```
python primo_ordine/driver.py primo_ordine/config/prova.yaml
```

### ⛔ **NESSUN'ALTRA VIA.** Nessun flag che cambi un parametro, nessuna variabile
d'ambiente, ### **nessun default nel codice** — e un argomento in piu' e'
### **un errore**, non una comodita'.

### ⭐ **PERCHE' COSI' SECCO, ed e' la lezione di `CONFIG-1`:** l'era `1` ha
### **`140` costanti di modulo** piu' una riga di comando che ne ribaltava alcune, e
`CONFIG-1` ha misurato che ### **`28` leggi su `31` giravano SPENTE** in sei misure.
### ⛔ **La cura non e' un presidio sui flag: e' che non ci siano flag.**

### ⚠ **E NESSUNO LO IMPORTA: `P-E4` lo impedisce.** `stato`, `termini/`,
`hamiltoniana`, `passo`, `crescita` e `vuoto` ### **non importano `driver` ne'
`osservatori/`** — ### **lo strumento non e' fisica** *(`A17`)*.
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
for _p in (_QUI, os.path.join(_QUI, "config"), os.path.join(_QUI, "leggi"),
           os.path.join(RADICE, "csv")):
    sys.path.insert(0, _p)

import numpy as np                                           # noqa: E402

import hamiltoniana as HAM                                   # noqa: E402
import passo as PA                                           # noqa: E402
import schema_config as CFG                                  # noqa: E402
import stato as ST                                           # noqa: E402

NL = chr(10)


def grafo(scena, nodi):
    """### Gli archi della scena. ### **Due scene, a vocabolario chiuso.**

    ### ⚠ **E NESSUNA POSIZIONE:** la scena dice ### **chi e' legato a chi**, non
    ### **dove sta** — `A17`, e la decisione `9` e' ### **APERTA.**
    """
    if scena == "catena":
        return np.arange(nodi - 1, dtype=int), np.arange(1, nodi, dtype=int)
    if scena == "anello":
        return (np.arange(nodi, dtype=int),
                (np.arange(nodi, dtype=int) + 1) % nodi)
    raise AssertionError("scena %r fuori vocabolario: lo schema doveva fermarla" % scena)


def termini_attivi(c):
    """### I termini ### **che la configurazione nomina, PER ID** *(punto `15(c)`)*.

    ### ⛔ **Un termine sul disco che la configurazione non nomina NON GIRA**, e
    ### **non c'e' nessun flag che lo accenda.**
    """
    tutti = HAM.carica_termini()
    per = {m.LEGGE: m for m in tutti}
    manca = [i for i in c["leggi_attive"] if i not in per]
    assert not manca, ("### LA CONFIGURAZIONE NOMINA LEGGI CHE NON SONO GENERATE: %s"
                       % manca)
    return [per[i] for i in sorted(c["leggi_attive"])]


def osservatori_attivi(c):
    import importlib.util
    d = os.path.join(_QUI, "osservatori")
    fuori = {}
    for f in sorted(os.listdir(d)):
        if not f.endswith(".py") or f == "__init__.py":
            continue
        spec = importlib.util.spec_from_file_location("_o_" + f[:-3],
                                                      os.path.join(d, f))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        if hasattr(m, "LEGGE"):
            fuori[m.LEGGE] = m
    manca = [i for i in c["osservatori"] if i not in fuori]
    assert not manca, ("### LA CONFIGURAZIONE NOMINA OSSERVATORI CHE NON ESISTONO: %s"
                       % manca)
    return [fuori[i] for i in sorted(c["osservatori"])]


def gira(c):
    """### Il giro, ### **con TUTTO dalla configurazione.**"""
    T = termini_attivi(c)
    OS_ = osservatori_attivi(c)
    ii, jj = grafo(c["scena"], c["nodi"])
    strati = PA.strati(ii, jj)
    st = ST.nuovo(c["nodi"])
    rng = np.random.default_rng(c["seme"])
    for k in st:
        st[k][...] = (rng.normal(size=st[k].shape)
                      + 1j * rng.normal(size=st[k].shape))
    avanza = PA.passo_locale if c["integratore"] == "locale" else PA.passo_globale
    kw = (strati,) if c["integratore"] == "locale" else ()
    misure0 = [(m.LEGGE, m.misura(st)) for m in OS_]
    e0 = HAM.energia(st, ii, jj, T)
    for _ in range(c["passi"]):
        st = avanza(st, ii, jj, c["dt"], T, c["iterazioni"], c["toll"], *kw)[0]
    misure1 = [(m.LEGGE, m.misura(st)) for m in OS_]
    e1 = HAM.energia(st, ii, jj, T)
    return {"stato": st, "archi": (ii, jj), "strati": len(strati),
            "misure0": misure0, "misure1": misure1, "energia0": e0, "energia1": e1}


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    # ### ⛔ **UN SOLO ARGOMENTO, e un argomento in piu- e- UN ERRORE.**
    if len(argv) != 1:
        print(__doc__.split("```")[1].strip())
        print("  ### LA RIGA DI COMANDO SCEGLIE SOLO IL FILE: un argomento, "
              "non %d" % len(argv))
        return 2
    c = CFG.carica(argv[0])
    imp = CFG.impronta(c)
    print("  la configurazione: %s   ### IMPRONTA %s" % (argv[0], imp))
    print("  %s" % "   ".join("%s=%s" % (k, c[k]) for k in CFG.CAMPI
                              if k not in ("versione",)))
    r = gira(c)
    print("  %d strati su %d archi" % (r["strati"], len(r["archi"][0])))
    for (n0, v0), (n1, v1) in zip(r["misure0"], r["misure1"]):
        assert n0 == n1
        rel = abs(v1 - v0) / max(abs(v0), 1e-300)
        print("  %-14s %.15f -> %.15f   relativa %.3e" % (n0, v0, v1, rel))
    rel = abs(r["energia1"] - r["energia0"]) / max(abs(r["energia0"]), 1e-300)
    print("  %-14s %+.12f -> %+.12f   relativa %.3e"
          % ("energia", r["energia0"], r["energia1"], rel))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
