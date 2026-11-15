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
    _STATO["secondo"] = False
    _STATO["fma"] = None
    MOTORE = "nucleo"


def stato():
    """### Per il registro *(M4)*: il motore, i fili, le chiamate del ciclo, i ripieghi, `sys.executable`."""
    import sys
    return {"motore": MOTORE, "fili": _STATO["fili"], "chiamate": _STATO["chiamate"], "ripieghi": _STATO["ripieghi"], "numba_importato": "numba" in sys.modules, "sys.executable": sys.executable,
            "secondo_passo": _STATO.get("secondo", False), "fma": _STATO.get("fma")}


# =====================================================================================
#   IL SECONDO PASSO (W3, Luca 2026-11-15 19:12): i cicli elemento per elemento
# =====================================================================================
# ### Le TRE funzioni: `flussi_parziali._grover_mezzo`, `flussi_parziali._hop_psi_mezzo`, `motore.Motore._ruota_attorno_a_n`.
# ### LA REGOLA DEL BIT (N1, W3): in numpy restano i PESI (`z`, `w = (1 - z)/grado`, `alpha`, `beta`) e `sin`/`cos` (le stesse
# ### chiamate di oggi); nel ciclo numba SOLO prodotti e somme complesse, nell'ORDINE di numpy, con il reale reso complesso
# ### `(x + 0j)` dove numpy lo promuove, e l'einsum accumulato da zero. Se D2 non e' al bit: la differenza e il perche'.
# ### LA PROVA DI H1 (Luca 2026-11-15 23:36): `fma` vero compila i tre cicli con fastmath={'contract'} -- SOLO la fusione in FMA,
# ### nessun'altra licenza (niente reassoc, nnan, ninf, nsz, arcp, afn); la cache solo per la versione senza.
def _costruisci2(fma):
    from numba import njit, prange
    fm = {"contract"} if fma else False
    ca = not fma

    @njit(parallel=True, fastmath=fm, error_model="numpy", cache=ca)
    def k_grover(vista, S, w, z, nodo):
        c = vista.shape[1]
        for e in prange(vista.shape[0]):
            kk = nodo[e]
            for q in range(c):
                presa = S[kk, q] * w[kk, 0]
                v = vista[e, q] * z[kk, 0]
                vista[e, q] = presa + v

    @njit(parallel=True, fastmath=fm, error_model="numpy", cache=ca)
    def k_hop(v, U, al, be):
        for a in prange(v.shape[0]):
            t0 = v[a, 0, 0]
            t1 = v[a, 0, 1]
            A = al[a, 0]
            B = be[a, 0]
            # ### lato 0 nuovo: alpha v0 + beta (U^dagger v1); l'einsum "aji,aj->ai": per i, la somma su j da zero
            m0 = 0j
            m0 = m0 + U[a, 0, 0].conjugate() * v[a, 1, 0]
            m0 = m0 + U[a, 1, 0].conjugate() * v[a, 1, 1]
            m1 = 0j
            m1 = m1 + U[a, 0, 1].conjugate() * v[a, 1, 0]
            m1 = m1 + U[a, 1, 1].conjugate() * v[a, 1, 1]
            m0 = m0 * B
            m1 = m1 * B
            v[a, 0, 0] = t0 * A + m0
            v[a, 0, 1] = t1 * A + m1
            # ### lato 1 nuovo: alpha v1 + beta (U v0), v0 dalla copia; l'einsum "aij,aj->ai"
            n0 = 0j
            n0 = n0 + U[a, 0, 0] * t0
            n0 = n0 + U[a, 0, 1] * t1
            n1 = 0j
            n1 = n1 + U[a, 1, 0] * t0
            n1 = n1 + U[a, 1, 1] * t1
            n0 = n0 * B
            n1 = n1 * B
            v[a, 1, 0] = v[a, 1, 0] * A + n0
            v[a, 1, 1] = v[a, 1, 1] * A + n1

    @njit(parallel=True, fastmath=fm, error_model="numpy", cache=ca)
    def k_ruota(psi, nn, s, c):
        uno_j = 1j
        meno_j = -1j
        for e in prange(psi.shape[0]):
            nx = complex(nn[e, 0], 0.0)
            ny = complex(nn[e, 1], 0.0)
            nz = complex(nn[e, 2], 0.0)
            p0 = psi[e, 0]
            p1 = psi[e, 1]
            a0 = nz * p0
            a0 = a0 + (nx - uno_j * ny) * p1
            a1 = (nx + uno_j * ny) * p0
            a1 = a1 - nz * p1
            m = meno_j * complex(s[e], 0.0)
            a0 = a0 * m
            a1 = a1 * m
            cc = complex(c[e], 0.0)
            p0 = p0 * cc
            p1 = p1 * cc
            psi[e, 0] = p0 + a0
            psi[e, 1] = p1 + a1
    return k_grover, k_hop, k_ruota


def accendi_secondo_passo(fma):
    """### **IL SECONDO PASSO** *(W3)*: con il motore numba GIA' acceso, sostituisce `_grover_mezzo`, `_hop_psi_mezzo`, `Motore._ruota_attorno_a_n`. Atomico; `spegni()` rimette tutto."""
    import flussi_parziali as FP                                 # ### una dipendenza VERA in piu' (la mappa)
    import motore
    assert MOTORE == "numba", "il secondo passo vuole il primo acceso (accendi_numba)"
    assert isinstance(fma, bool), "fma: True o False, scritto da chi chiama"
    k2 = _STATO.setdefault("k2", {})
    if fma not in k2:
        k2[fma] = _costruisci2(fma)
    kg, kh, kr = k2[fma]
    np = _numpy

    def _grover_mezzo(mot, vista, frazione):
        n, nodo = mot.inc.n, mot.inc.nodo
        c = vista.shape[1]
        S = mot._b("fp_S_campo_%d" % c, (n, c), vista.dtype)
        mot._somma_per_nodo(vista, S)
        z = FP.z_nodo(mot, frazione)
        w = mot._b("fp_w_grover", (n, 1), complex)
        np.subtract(1.0, z, out=w)
        np.divide(w, mot.inc.grado.reshape(-1, 1), out=w)
        kg(vista, S, w, z, nodo)
        return vista

    def _hop_psi_mezzo(mot, psi, frazione):
        m = mot.inc.m
        al, be = FP._alfa_beta(mot, FP.z_arco(mot, frazione))
        kh(psi.reshape(m, 2, 2), mot.geo.U, al, be)
        return psi

    def _ruota_attorno_a_n(self, psi, ang):
        s = self._b("sin", ang.shape, float)
        np.sin(ang, out=s)
        c = ang
        np.cos(ang, out=c)
        kr(psi, self.geo.n, s, c)
    try:
        for bersaglio, nome, nuova in ((FP, "_grover_mezzo", _grover_mezzo), (FP, "_hop_psi_mezzo", _hop_psi_mezzo), (motore.Motore, "_ruota_attorno_a_n", _ruota_attorno_a_n)):
            _STATO["originali"].append((bersaglio, nome, getattr(bersaglio, nome)))
            setattr(bersaglio, nome, nuova)
    except Exception:
        spegni()
        raise
    _STATO["secondo"] = True
    _STATO["fma"] = fma
    return {"secondo_passo": ["flussi_parziali._grover_mezzo", "flussi_parziali._hop_psi_mezzo", "motore.Motore._ruota_attorno_a_n"]}
