# -*- coding: utf-8 -*-
"""### **IL MOTORE NUMBA, CON UNO SWITCH** *(decisione di Luca `2026-11-15` `15:50`, `18:08`, `19:12`; la carta `doc/TASK_HISTORY/2026-11-15_motore_numba.md`, sez. `7`-`8`)*.

### ⭐ **LO SWITCH E' UN SOLO PUNTO: la variabile di modulo `MOTORE`** *(`"nucleo"` o `"numba"`)*, **cambiata SOLO da `accendi_numba(fili)` e da `spegni()`.**
**Spento per difetto: `MOTORE = "nucleo"`, e numba NON importato** *(questo modulo importa numba solo dentro `accendi_numba`: D1, `'numba' not in sys.modules`)*.

### **COME AGISCE** *(W1, Luca `19:12`)*: **`accendi_numba` SOSTITUISCE IN MEMORIA le funzioni del nucleo che contengono `np.add.at`** *(`SOSTITUITE`)*: **legge il loro SORGENTE** *(`inspect.getsource`, il file del ramo)*, **cambia SOLO `np.add.at(` in `_MN_add_at(`, e le ricompila nel namespace del loro modulo** *(la copia e' riga per riga come l'originale PER COSTRUZIONE)*.
**`_MN_add_at(fuori, idx, v)`: un ciclo numba sulle righe di uscita che somma gli indici in ordine CRESCENTE a partire dal valore che c'e'** *(l'ordine di `np.add.at`: le stesse operazioni IEEE, quindi AL BIT; le righe in parallelo, ognuna in sequenza: lo stesso risultato con qualunque numero di fili)*.
**Il ripiego dichiarato e CONTATO: i tipi o le forme diversi da quelli del ciclo -> il `np.add.at` di numpy.** **`spegni()` rimette gli oggetti funzione ORIGINALI** *(il collaudo: `is`)*.
### **Se numba non c'e': `accendi_numba` alza `ImportError` e la corsa NON parte** *(M4: mai un ripiego silenzioso sul motore di oggi)*. **La cache della compilazione: `NUMBA_CACHE_DIR`** *(N6: su E:, fuori dal repo; lo imposta chi chiama)*.
"""
import numpy as _numpy

MOTORE = "nucleo"
# ### le funzioni con np.add.at nel tick (W1): (il modulo, la classe o None, il nome)
SOSTITUITE = (("motore", "Motore", "_somma_per_nodo"), ("motore", "Motore", "elicita"), ("motore", "Motore", "densita_materia"),
              ("motore", "Motore", "densita_vuoto"), ("energia_pesata", None, "_per_nodo"), ("energia_pesata", None, "termini_di_h"))
_STATO = {"originali": [], "nucleo": None, "cache": {}, "fili": None, "chiamate": 0, "ripieghi": 0}


def _costruisci():
    """### Il ciclo numba *(compilato alla prima chiamata, o dalla cache)*."""
    from numba import njit, prange

    @njit(parallel=True, fastmath=False, error_model="numpy", cache=True)
    def at_righe(fuori2, v2, ordine, inizio):
        K = inizio.shape[0] - 1
        c = fuori2.shape[1]
        for k in prange(K):
            a = inizio[k]
            b = inizio[k + 1]
            for q in range(c):
                s = fuori2[k, q]
                for j in range(a, b):
                    s = s + v2[ordine[j], q]
                fuori2[k, q] = s
    return at_righe


def _ordine_di(idx, K):
    """### L'ordine di `np.add.at`: per ogni riga gli indici in ordine CRESCENTE *(argsort stabile)* e gli inizi; tenuto per l'oggetto `idx`."""
    c = _STATO["cache"].get(id(idx))
    if c is not None and c[0] is idx and c[1] == K:
        return c[2], c[3]
    ordine = _numpy.argsort(idx, kind="stable").astype(_numpy.int64)
    conti = _numpy.bincount(idx, minlength=K)
    inizio = _numpy.zeros(K + 1, dtype=_numpy.int64)
    _numpy.cumsum(conti, out=inizio[1:])
    _STATO["cache"][id(idx)] = (idx, K, ordine, inizio)
    return ordine, inizio


def add_at(fuori, idx, v):
    """### **`np.add.at(fuori, idx, v)` col ciclo numba**, o il ripiego dichiarato e contato *(il `np.add.at` di numpy)*."""
    v = _numpy.asarray(v)
    ok = (_STATO["nucleo"] is not None and isinstance(fuori, _numpy.ndarray) and isinstance(idx, _numpy.ndarray) and idx.ndim == 1
          and idx.dtype.kind in "iu" and fuori.flags.c_contiguous and v.dtype == fuori.dtype and v.shape == (idx.shape[0],) + fuori.shape[1:]
          and fuori.dtype.kind in "fc")
    if not ok:
        _STATO["ripieghi"] += 1
        return _numpy.add.at(fuori, idx, v)
    K = fuori.shape[0]
    ordine, inizio = _ordine_di(idx, K)
    _STATO["nucleo"](fuori.reshape(K, -1), _numpy.ascontiguousarray(v).reshape(idx.shape[0], -1), ordine, inizio)
    _STATO["chiamate"] += 1
    return None


def _ricompila(mod, nome):
    """### La funzione `nome` del modulo `mod` *(o il metodo, dedentato)* dal suo sorgente, con `np.add.at(` -> `_MN_add_at(`, compilata coi GLOBALI del modulo."""
    import inspect
    import textwrap
    oggetto = getattr(mod, nome) if "." not in nome else getattr(getattr(mod, nome.split(".")[0]), nome.split(".")[1])
    src = textwrap.dedent(inspect.getsource(oggetto))
    n = src.count("np.add.at(")
    assert n >= 1, "%s.%s NON contiene np.add.at: non e' da sostituire" % (mod.__name__, nome)
    src = src.replace("np.add.at(", "_MN_add_at(")
    corto = nome.split(".")[-1]
    salvo = mod.__dict__.get(corto, _numpy)
    codice = compile(src, inspect.getsourcefile(oggetto), "exec")
    exec(codice, mod.__dict__)
    nuova = mod.__dict__[corto]
    if "." in nome:                                             # ### un METODO: il nome nel modulo torna com'era
        if salvo is _numpy:
            del mod.__dict__[corto]
        else:
            mod.__dict__[corto] = salvo
    return oggetto, nuova, n


def accendi_numba(fili):
    """### **ACCENDE il motore numba**: importa numba *(se manca: `ImportError`, la corsa NON parte)*, fissa i fili *(N5)*, costruisce il ciclo, SOSTITUISCE le funzioni di `SOSTITUITE`. `fili` OBBLIGATORIO."""
    global MOTORE
    import numba
    import energia_pesata                                       # ### le dipendenze VERE, scritte (P-MOD; la mappa): importate solo qui, all'accensione
    import motore
    moduli = {"motore": motore, "energia_pesata": energia_pesata}
    if MOTORE == "numba":
        spegni()
    numba.set_num_threads(int(fili))
    _STATO["fili"] = numba.get_num_threads()
    if _STATO["nucleo"] is None:
        _STATO["nucleo"] = _costruisci()
    righe = []
    try:                                                        # ### ATOMICA (W2, 2026-11-15): se una sostituzione cade, si rimettono TUTTE le originali e l'errore sale
        for modulo, classe, nome in SOSTITUITE:
            mod = moduli[modulo]
            mod.__dict__["_MN_add_at"] = add_at
            orig, nuova, n = _ricompila(mod, nome if classe is None else "%s.%s" % (classe, nome))
            bersaglio = mod if classe is None else getattr(mod, classe)
            _STATO["originali"].append((bersaglio, nome, orig))
            setattr(bersaglio, nome, nuova)
            righe.append("%s.%s%s (%d np.add.at)" % (modulo, "" if classe is None else classe + ".", nome, n))
    except Exception:
        spegni()
        raise
    MOTORE = "numba"
    return {"motore": MOTORE, "fili": _STATO["fili"], "numba": numba.__version__, "sostituite": righe}


def spegni():
    """### **SPEGNE**: rimette gli oggetti funzione ORIGINALI; `MOTORE = "nucleo"`."""
    global MOTORE
    import sys
    for bersaglio, nome, orig in reversed(_STATO["originali"]):
        setattr(bersaglio, nome, orig)
    _STATO["originali"].clear()
    for modulo in sorted(set(m for m, _c, _n in SOSTITUITE)):
        if modulo in sys.modules:
            sys.modules[modulo].__dict__.pop("_MN_add_at", None)
    MOTORE = "nucleo"


def stato():
    """### Per il registro *(M4)*: il motore, i fili, le chiamate del ciclo, i ripieghi, `sys.executable`."""
    import sys
    return {"motore": MOTORE, "fili": _STATO["fili"], "chiamate": _STATO["chiamate"], "ripieghi": _STATO["ripieghi"], "numba_importato": "numba" in sys.modules, "sys.executable": sys.executable}
