# -*- coding: utf-8 -*-
"""IL SIGILLO DI `Z43` CURA (2): `r = cs_nodo / CS_M`, l'orologio a luce.

*(Decisione di Luca del 2026-10-05. I **sette criteri** sono fissati in
`doc/TASK_HISTORY/2026-10-05_z43-cura2-r-da-cs.md`, committato **prima** in `012f419`.)*

### I SETTE CRITERI
| | che cosa pretende | e se fallisce |
|---|---|---|
| **`0`** | **braccio 0**: il *prima* + la patch committata = **il blob di oggi**, al byte | ### **FERMO** |
| **`1`** | ### **`FEDELTA'`**: il `r` restituito `== _cs_nodo_prev / CS_M` **AL BIT** | ### **FERMO** |
| **`2`** | ### **NIENTE ALTALENA, PER COPPIA DI PASSI:** `<= 1.2` su **OGNI** coppia dal passo `3` | ### **FERMO** |
| **`3`** | **autocorrelazione a ritardo 1** della mediana di `r` **non fortemente negativa** | ### **FERMO** |
| **`4`** | ### **SEGNO:** `r` mediano nella **materia** *(top `5 %` di `abs(psi)^2`)* **MINORE** che nel **vuoto** *(bottom `25 %`)*. ### **E' FEDELTA', non fisica** | si **riporta** |
| **`5`** | ### **LOCALITA', MISURATA:** `cs` di un nodo distante quando se ne perturba **UNO**. Atteso **non zero**, `~1/n` | si **riporta** |
| **`6`** | ### **CASO CHE DEVE FALLIRE:** lo stato **diverge** da quello della `PARTE A`, e **da QUALE passo** | ### **FERMO** |
| **`7`** | **`150` passi senza `FERMO`**, e che cosa cambia **a valle** | ### **FERMO** |

### IL CRITERIO `2` SI LEGGE **PER COPPIA**, ed e' la correzione del guardiano (`b337ec1`)
Il rapporto **aggregato su tutta la corsa NASCONDE L'INIZIO**: una mediana su `150` passi
con una coda lunga e quieta schiaccia un inizio violento. ### **Quindi: `<= 1.2` su OGNI
coppia dal passo `3` in poi**, escluse **solo** le coppie in cui la cache di `cs` non e'
allineata *(**contate e dichiarate**)*; l'aggregato si riporta ### **ma non basta da solo.**

### ⚠ **UNA COSA CHE IL CRITERIO `2`, COME E' SCRITTO, NON VEDE -- e la riporto accanto
### invece di sostituirla:** `<= 1.2` e' **a UN LATO SOLO**. Un'alternanza in cui il passo
**dispari** e' piu' BASSO del pari da' un rapporto `< 1` e **passa**, pur essendo
un'altalena. ### **Il criterio e' di Luca e non lo reinterpreto:** applico quello, e
**accanto** riporto `max(rapporto, 1/rapporto)`, che e' la lettura a DUE lati.
### **Se i due verdetti divergessero, la cosa da guardare e' quella.**

### LA SOGLIA DEL CRITERIO `3` LA SCELGO IO, E LO DICHIARO
Il mandato dice <<non fortemente negativa>> **senza un numero**. Fisso
**`autocorr >= -0.5`**, ### **PRIMA di vedere i dati**: un'alternanza perfetta a periodo `2`
da' `-1`, e `-0.5` e' il punto di mezzo. ### **Il numero si riporta comunque**, qualunque
sia il verdetto: la soglia decide il `FERMO`, non che cosa si scrive.

### L'ANELLO HA **DUE** CAMMINI, e il criterio `3` li copre **entrambi**
*(annotazione del guardiano, 2026-10-05)*. Non uno:
1. ### **`cs -> r -> dt_e -> cs`** -- `r` entra nel tempo d'arco, `dt_e` nei sotto-passi
   della metrica, la metrica in `cs`;
2. ### **`r -> _dts dell'orologio -> fase di _psi_spinor -> interferenza in psi ->
   abs(psi)^2 -> cs -> r`** -- `r` entra nel tic dell'orologio di Compton, l'orologio nella
   **fase** dello spinore, la fase nell'**interferenza** che costruisce `psi`, e
   `abs(psi)^2` **E' la densita' da cui `cs` nasce.**
### **L'autocorrelazione a ritardo 1 della mediana di `r` non distingue i due cammini: li
### vede SOMMATI.** Per questo il criterio `3` **ferma su entrambi**, e per questo
### **nominarli e' parte del referto:** se oscilla, il passo dopo e' **capire quale**.

### IL CRITERIO `4` E' UN CONTROLLO DI **FEDELTA'**, NON UN RISULTATO DI FISICA
*(annotazione del guardiano, 2026-10-05)*. `r` **materia** `<` `r` **vuoto** ### **SEGUE
DALLA FORMULA di `_cs_nodo`**: `cs_floor = CS_M/(1 + sqrt(I)*sqrt(1/scala))` **decresce in
`I`**, e la transizione `0.5*(1 + tanh(1 - u))` pure. ### **Quindi puo' fallire SOLO se il
codice e' sbagliato** -- e' un `FALSO-UNO` in attesa, non una predizione messa alla prova.
### **Nel referto va scritto come fedelta', e non si rivendica come conferma della fisica.**

### IL CRITERIO `5` E' NUOVO PER QUESTO REPO, e chiama **LA LEGGE STESSA**
`_cs_nodo(I, w)` due volte -- una su `I`, una su `I` con **un solo nodo perturbato** -- e il
cambiamento relativo si riporta ### **IN FUNZIONE DELLA DISTANZA SUL GRAFO**, non come un
numero solo: ### **un numero solo non distingue <<locale piu' una coda globale>> da
<<globale>>.** La forma della curva lo fa.
### ⚠ **E `_cs_nodo` incrementa `_cs_lam_degenere` se `mean(I) <= 1e-30`:** si **verifica
PRIMA** di chiamarla, e il contatore si **salva e si ripristina** comunque.
### **Una misura non muove cio' che misura, nemmeno un contatore.**

### L'ACCOPPIAMENTO `I` <-> `r` NON E' NELLO STESSO PASSO, e il criterio `4` lo rispetta
`r_t = cs_(t-1)/CS_M`, e `cs_(t-1)` viene da `I_(t-1)`: dentro un passo `ritmo()` gira
**PRIMA** di `_cs_nodo`. ### **Quindi `I` del passo `t` si accoppia con `r` del passo
`t+1`**, e confrontarli nello stesso passo sarebbe ### **sfasare di uno la misura del
segno.**

# ESENTE-H-P8: le occorrenze di `HEAD` in questo file stanno nella DOCSTRING di `braccio0()`
#   e dicono il CONTRARIO di cio' che il presidio teme: spiegano perche' il *prima* NON si
#   prende da `HEAD~1` ma dal PADRE DEL COMMIT CHE HA CAMBIATO IL SIMULATORE. Potevo
#   scrivere `@~1`, che passa il controllo: NON LO FACCIO -- sarebbe disarmare un presidio
#   cambiando le parole. E' la QUARTA volta per la stessa ragione.
# ESENTE-H-P3: la COPIA PATCHATA serve ai criteri 1 e 5. Il `r` restituito da `ritmo()` e il
#   `_csp` che ha letto NON sono osservabili da fuori (dopo il passo `_cs_nodo_prev` e' GIA'
#   stato riscritto nello stesso passo), e `I`/`w` vivono dentro il corpo di `step`:
#   ricostruirli fuori sarebbe una SECONDA scrittura della stessa legge (`9-ter`). La scena
#   passa TUTTA dal CLI, e la configurazione INTERA si DICHIARA.
"""
import contextlib
import hashlib
import io
import json
import os
import platform
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _cli_flag   # noqa: E402
import _passo      # noqa: E402

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_z43_cura2")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PATCH = os.path.join(RADICE, "csv", "_seal_fork", "_z43_cura2_patch.py")
PASSI = 150
SOGLIA_ALTALENA = 1.2          # il criterio di Luca, a UN lato
SOGLIA_AUTOCORR = -0.5         # LA SCELGO IO, e lo dichiaro nella docstring
PASSI_COPPIA = (4, 10, 20, 30, 40, 60, 100, 140)   # quelli chiesti dalla correzione

P = []


def stampa(s=""):
    print(s)
    P.append(s)


def riga(c="-"):
    stampa(c * 104)


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, cwd=RADICE)


def piattaforma():
    return {"python": platform.python_version(), "numpy": np.__version__,
            "sistema": platform.system() + " " + platform.release(),
            "macchina": platform.machine()}


def _timbro():
    return {"strumento": os.path.basename(__file__), "blob": blob(__file__)}


# =============================================================== IL COMPARATORE
# ### QUARTA COPIA dello stesso comparatore, e LO DICHIARO: e' la voce
#   `SIGILLO-COMPARATORE-DUPLICATO`, ora con QUATTRO copie. La cura giusta e' estrarlo in un
#   modulo comune, e NON si fa dentro il lavoro di un altro mandato.
#   ### Lo scarto si misura SOLO sulle celle FINITE: `inf - inf` ALZA (il simulatore mette
#   `np.seterr` a raise) -- e' il difetto che ha ucciso il sigillo di `MEM_FASE` al passo 61.

def _vettori_di(v):
    if hasattr(v, "bit_generator"):
        return ("rng", v.bit_generator.state)
    if all(hasattr(v, k) for k in ("data", "indices", "indptr", "shape")):
        return ("sparsa", (tuple(v.shape), np.asarray(v.data),
                           np.asarray(v.indices), np.asarray(v.indptr)))
    return None


def _rng_uguale(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return set(a) == set(b) and all(_rng_uguale(a[k], b[k]) for k in a)
    if isinstance(a, np.ndarray):
        return bool(a.shape == b.shape and np.array_equal(a, b))
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(_rng_uguale(x, y) for x, y in zip(a, b))
    return bool(a == b)


def confronta(x, y):
    """-> `(uguale, quanti, nota, max_scarto)`. `NaN` contro `NaN` e' UGUALE."""
    vx, vy = _vettori_di(x), _vettori_di(y)
    if vx is not None or vy is not None:
        if vx is None or vy is None or vx[0] != vy[0]:
            return False, -1, "tipi strutturati diversi", None
        if vx[0] == "rng":
            ug = _rng_uguale(vx[1], vy[1])
            return ug, (0 if ug else 1), ("" if ug else "generatore diverso"), None
        fa, fb = vx[1], vy[1]
        if fa[0] != fb[0]:
            return False, -1, "forme diverse", None
        tot, mx = 0, 0.0
        for ca, cb in zip(fa[1:], fb[1:]):
            ug, nd, _n, m = confronta(ca, cb)
            if not ug:
                tot += (nd if nd >= 0 else 1)
                if m is not None:
                    mx = max(mx, m)
        return tot == 0, tot, ("" if tot == 0 else "sparsa diversa"), mx
    if isinstance(x, np.ndarray) or isinstance(y, np.ndarray):
        a, b = np.asarray(x), np.asarray(y)
        if a.shape != b.shape:
            return False, -1, "forme diverse: %s contro %s" % (a.shape, b.shape), None
        if a.dtype.kind in "fc" and b.dtype.kind in "fc":
            af, bf = np.asarray(a, complex), np.asarray(b, complex)
            ug = (af == bf) | (np.isnan(af) & np.isnan(bf))
            nd = int(np.sum(~ug))
            mx, nonfin = 0.0, 0
            if nd:
                fin = np.isfinite(af) & np.isfinite(bf)
                sel = fin & ~ug
                nonfin = int(np.sum(~fin & ~ug))
                with np.errstate(all="ignore"):
                    mx = (float(np.max(np.abs(af[sel] - bf[sel])))
                          if bool(np.any(sel)) else None)
            nota = ("" if not nonfin else "%d celle diverse NON FINITE" % nonfin)
            return nd == 0, nd, nota, mx
        ug = (a == b)
        nd = int(np.sum(~np.asarray(ug)))
        return nd == 0, nd, "", None
    if isinstance(x, dict) or isinstance(y, dict):
        if not (isinstance(x, dict) and isinstance(y, dict)):
            return False, -1, "uno e' un dizionario e l'altro no", None
        if set(x) != set(y):
            return False, -1, "chiavi diverse", None
        tot, mx = 0, 0.0
        for k in x:
            ug, nd, _n, m = confronta(x[k], y[k])
            if not ug:
                tot += (nd if nd >= 0 else 1)
                if m is not None:
                    mx = max(mx, m)
        return tot == 0, tot, ("" if tot == 0 else "dizionario diverso"), mx
    try:
        return (x == y), (0 if x == y else 1), "", None
    except Exception as e:
        return False, -1, "non confrontabile: %r" % (e,), None


def classe(nome):
    if nome.startswith("_g_") or nome.startswith("_ritmo_") or nome.startswith("_tum_") \
            or nome.startswith("_cs_lam") or nome.startswith("_smp_") \
            or nome.startswith("_cs_in_") or nome in ("_veleno_registro",):
        return "contatore/registro"
    return "STATO"


def confronta_reti(n1, n2):
    k1, k2 = set(vars(n1)), set(vars(n2))
    out = []
    for nome in sorted(k1 | k2):
        if nome not in k1 or nome not in k2:
            out.append({"nome": nome, "classe": classe(nome), "quanti": -1,
                        "nota": "presente solo in uno dei due", "max_scarto": None})
            continue
        ug, nd, nota, mx = confronta(getattr(n1, nome), getattr(n2, nome))
        if not ug:
            out.append({"nome": nome, "classe": classe(nome), "quanti": nd,
                        "nota": nota, "max_scarto": mx})
    return out


# =============================================================== LA COPIA, per i criteri 1 e 5
def copia_patchata():
    """Una COPIA del sorgente CURATO con DUE punti di verifica.

    ### `r` e il `_csp` che `ritmo()` ha letto NON sono osservabili da fuori: dopo il passo
    ### `_cs_nodo_prev` e' GIA' stato riscritto NELLO STESSO passo. E `I`/`w` vivono dentro
    ### il corpo di `step`. Ricostruirli fuori sarebbe una SECONDA scrittura della legge.
    """
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    dst = os.path.join(FUORI, "_sim_gancio.py")
    t = io.open(SIM, encoding="utf-8").read()
    fatte = []

    def uno(a, b, et):
        nonlocal t
        n = t.count(a)
        if n != 1:
            raise SystemExit("[FERMO] l'ancora di `%s` compare %d volte, non 1." % (et, n))
        t = t.replace(a, b)
        fatte.append(et)

    uno("import numpy as np" + NL,
        "import numpy as np" + NL
        + "_MIS = None   # [SIGILLO Z43 CURA 2] lo riempie lo strumento" + NL,
        "il gancio di modulo `_MIS`")
    # ### il punto di verifica del criterio 1: l'ULTIMA riga di `ritmo()`.
    uno("        return np.asarray(_csp, float)[:self.n] / CS_M" + NL,
        "        _r_out = np.asarray(_csp, float)[:self.n] / CS_M" + NL
        + "        if _MIS is not None:" + NL
        + "            _MIS.ritmo(self, csp=_csp, r=_r_out)" + NL
        + "        return _r_out" + NL,
        "il punto di verifica di `ritmo()`, sul valore RESTITUITO")
    # ### il punto del criterio 5: `I` e `w` dallo STESSO istante in cui la legge li vede.
    uno("            cs_nodo = self._cs_nodo(I, w)" + NL,
        "            cs_nodo = self._cs_nodo(I, w)" + NL
        + "            if _MIS is not None:" + NL
        + "                _MIS.densita(self, I=I, w=w, cs_nodo=cs_nodo)" + NL,
        "il punto di cattura di `I` e `w`, al sito di `_cs_nodo`")
    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return dst, fatte


class Misura(object):
    """`CRITERIO 1` (fedelta' AL BIT) e la cattura per il `CRITERIO 5`."""

    def __init__(self, CS_M):
        self.CS_M = float(CS_M)
        self.passo = 0
        self.chiamate = 0
        self.nodi = 0
        self.diversi = 0
        self.chiamate_diverse = 0
        self.max_scarto = 0.0
        self.peggiore = None
        self.ultimo_I = None
        self.ultimo_w = None
        self.ultimo_I_passo = None

    def ritmo(self, net, csp, r):
        self.chiamate += 1
        atteso = np.asarray(csp, float)[:net.n] / self.CS_M
        o = np.asarray(r, float)
        self.nodi += int(len(o))
        ug = (o == atteso) | (np.isnan(o) & np.isnan(atteso))
        nd = int(np.sum(~ug))
        if nd:
            self.diversi += nd
            self.chiamate_diverse += 1
            fin = np.isfinite(o) & np.isfinite(atteso)
            sel = fin & ~ug
            with np.errstate(all="ignore"):
                sc = (float(np.max(np.abs(o[sel] - atteso[sel])))
                      if bool(np.any(sel)) else None)
            if sc is not None and sc > self.max_scarto:
                self.max_scarto = sc
                self.peggiore = {"passo": self.passo, "nodi_diversi": nd,
                                 "nodi": int(len(o)), "max_scarto": sc}

    def densita(self, net, I, w, cs_nodo):
        # si tiene SOLO l'ultimo: serve al criterio 5, che gira a corsa finita
        self.ultimo_I = np.array(I, float, copy=True)
        self.ultimo_w = np.array(w, float, copy=True)
        self.ultimo_I_passo = self.passo


# =============================================================== BRACCIO 0
def braccio0():
    """### IL *PRIMA* VIENE DAL PADRE DEL COMMIT CHE HA CAMBIATO IL SIMULATORE.

    ### **NON `HEAD~1`:** dopo il commit della cura ne arriva un altro, e `HEAD~1` diventa
    **il commit della cura** -- il *prima* estratto sarebbe ### **GIA' CURATO.** Lo trovo' il
    sigillo di `VELENO-ARCHI-KEEP` rifiutandosi di proseguire *(`c7f2eb3`)*.
    ### **E il *prima* si verifica contro quello che LA PATCH DICHIARA.**
    """
    out = {"dove": "il PADRE del commit CHE HA CAMBIATO IL SIMULATORE (H-P8)"}
    rc = git("log", "-1", "--format=%H", "--", "soliton_simulator.py")
    commit_cura = rc.stdout.decode().strip()
    out["commit_che_ha_cambiato_il_simulatore"] = commit_cura
    r = git("rev-parse", commit_cura + "^")
    padre = r.stdout.decode().strip()
    out["padre"] = padre
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    dst = os.path.join(FUORI, "_sim_prima.py")
    g = git("cat-file", "-p", padre + ":soliton_simulator.py")
    if g.returncode != 0:
        out["stato"] = "non estratto: %r" % (g.stderr[:200],)
        return None, out
    io.open(dst, "wb").write(g.stdout)
    out["blob_prima"] = blob(dst)[:8]
    _ps = io.open(PATCH, encoding="utf-8").read()
    _m = [x for x in _ps.split(NL) if x.startswith("BLOB_PRIMA = ")]
    out["blob_prima_atteso"] = (_m[0].split("=", 1)[1].strip().strip(chr(34))
                                if _m else None)
    out["prima_e_quello_atteso"] = bool(out["blob_prima"] == out["blob_prima_atteso"])
    if not out["prima_e_quello_atteso"]:
        out["stato"] = ("il *prima* estratto (%s) non e' quello che la patch dichiara (%s)"
                        % (out["blob_prima"], out["blob_prima_atteso"]))
        return None, out
    out["blob_patch"] = blob(PATCH)[:8]
    patchato = os.path.join(FUORI, "_sim_patchato.py")
    pr = subprocess.run([sys.executable, PATCH, dst, patchato],
                        capture_output=True, cwd=RADICE)
    out["patch_returncode"] = pr.returncode
    out["blob_patchato"] = blob(patchato)[:8] if os.path.isfile(patchato) else None
    out["blob_oggi"] = blob(SIM)[:8]
    out["coincide"] = bool(out["blob_patchato"] == out["blob_oggi"])
    out["stato"] = "fatto"
    return dst, out


# =============================================================== IL CRITERIO 5: LOCALITA'
def distanze(net, sorgente, salti):
    """BFS sul GRAFO DEGLI ARCHI, fino a `salti`. -> array di distanze (-1 = non raggiunto)."""
    n = int(net.n)
    ii = np.asarray(net.i)
    jj = np.asarray(net.j)
    m = (ii < n) & (jj < n)
    ii, jj = ii[m], jj[m]
    d = np.full(n, -1, int)
    d[sorgente] = 0
    fronte = np.array([sorgente])
    for k in range(1, salti + 1):
        sel = np.isin(ii, fronte)
        vicini = jj[sel]
        sel2 = np.isin(jj, fronte)
        vicini = np.concatenate([vicini, ii[sel2]])
        vicini = np.unique(vicini)
        nuovi = vicini[d[vicini] < 0]
        if not len(nuovi):
            break
        d[nuovi] = k
        fronte = nuovi
    return d


def localita(net, I, w, CS_M, salti=6):
    """### CHIAMA LA LEGGE STESSA due volte: una su `I`, una su `I` con UN nodo perturbato.

    Il contatore `_cs_lam_degenere` si **salva e si ripristina**: una misura non muove cio'
    che misura, ### **nemmeno un contatore.**
    """
    out = {"salti": salti}
    n = int(net.n)
    I = np.asarray(I, float)
    lam = float(np.mean(np.maximum(I[:n], 0.0))) if n else 0.0
    out["mean_I"] = lam
    out["n"] = n
    out["uno_su_n"] = (1.0 / n) if n else None
    # ### IL PRE-CONTROLLO, prima di chiamare: se `mean(I) <= 1e-30` NON si chiama.
    if not (lam > 1e-30):
        out["stato"] = "SALTATO: mean(I) = %.3e <= 1e-30, chiamarla alzerebbe il contatore" % lam
        return out
    prima = getattr(net, "_cs_lam_degenere", None)
    # il nodo da perturbare: il PIU' DENSO, perche' e' dove la perturbazione e' piu' grande
    sorg = int(np.argmax(I[:n]))
    out["nodo_perturbato"] = sorg
    out["I_del_nodo"] = float(I[sorg])
    cs0 = np.asarray(net._cs_nodo(I, w), float)
    Ip = I.copy()
    Ip[sorg] = I[sorg] * 2.0            # RADDOPPIO: un fattore, non un numero tarato
    out["perturbazione"] = "I del nodo piu' denso RADDOPPIATO (x2: un fattore, non un numero)"
    cs1 = np.asarray(net._cs_nodo(Ip, w), float)
    dopo = getattr(net, "_cs_lam_degenere", None)
    out["contatore_prima"] = prima
    out["contatore_dopo"] = dopo
    out["contatore_mosso"] = bool(prima != dopo)
    if prima is None:
        if hasattr(net, "_cs_lam_degenere"):
            del net._cs_lam_degenere
    else:
        net._cs_lam_degenere = prima
    out["contatore_ripristinato"] = getattr(net, "_cs_lam_degenere", None)
    with np.errstate(all="ignore"):
        rel = np.abs(cs1 - cs0) / np.maximum(np.abs(cs0), 1e-300)
    d = distanze(net, sorg, salti)
    out["per_distanza"] = []
    for k in range(0, salti + 1):
        sel = (d == k)
        if not bool(np.any(sel)):
            continue
        out["per_distanza"].append({
            "distanza": k, "nodi": int(np.sum(sel)),
            "mediana_cambio_rel": float(np.median(rel[sel])),
            "max_cambio_rel": float(np.max(rel[sel])),
            "rapporto_su_1_su_n": (float(np.median(rel[sel])) * n) if n else None})
    sel = (d < 0)
    if bool(np.any(sel)):
        out["oltre_%d_salti" % salti] = {
            "nodi": int(np.sum(sel)),
            "mediana_cambio_rel": float(np.median(rel[sel])),
            "max_cambio_rel": float(np.max(rel[sel])),
            "rapporto_su_1_su_n": float(np.median(rel[sel])) * n}
    out["stato"] = "fatto"
    return out


# =============================================================== LA SCENA
def carica(nome, sim):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net, a


def _scrivi(d):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    io.open(os.path.join(FUORI, "sigillo.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))
    io.open(os.path.join(FUORI, "sigillo.txt"), "w", encoding="utf-8").write(
        NL.join(P) + NL)


def main(argv):
    passi = PASSI
    if "--collaudo" in argv[1:]:
        riga("=")
        stampa("IL COLLAUDO DEL SIGILLO DI Z43 CURA (2)")
        riga("=")
        return collaudo()
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    riga("=")
    stampa("IL SIGILLO DI Z43 CURA (2): r = cs_nodo / CS_M, l'orologio a luce")
    riga("=")
    stampa()
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa("  simulatore OGGI %s   patch %s   strumento %s"
           % (blob(SIM)[:8], blob(PATCH)[:8], blob(__file__)[:8]))
    stampa()
    vecchio, b0 = braccio0()
    riga("=")
    stampa("BRACCIO 0: il *prima* NON si asserisce, SI RICOSTRUISCE")
    riga("=")
    for k in ["commit_che_ha_cambiato_il_simulatore", "padre", "blob_prima",
              "blob_prima_atteso", "prima_e_quello_atteso", "blob_patch",
              "blob_patchato", "blob_oggi", "patch_returncode", "coincide", "stato"]:
        if k in b0:
            stampa("  %-38s %s" % (k, b0[k]))
    stampa()
    if vecchio is None or not b0.get("coincide"):
        stampa("### IL BRACCIO 0 NON TORNA. MI FERMO.")
        _scrivi({"braccio0": b0, "esito": 1, "piattaforma": pf,
                 "timbro_strumento": _timbro()})
        return 1

    dst, fatte = copia_patchata()
    stampa("  copia col gancio per i criteri 1 e 5: %s  blob %s  (%d ancore)"
           % (os.path.basename(dst), blob(dst)[:8], len(fatte)))
    for f in fatte:
        stampa("      - " + f)
    stampa()

    # ### TRE BRACCI, e la ragione l'ha trovata il primo giro del sigillo della PARTE A:
    #   `_calcpsi_origini` registra "funzione:NUMERO_DI_RIGA" di chi chiama `calcola_psi`, e
    #   un gancio SPOSTA le righe. Quindi NESSUN criterio confronta un patchato con un
    #   non-patchato: A e B sono entrambi NON patchati, C e' il patchato.
    SA, nA, a = carica("sim_z43b_A", vecchio)     # la PARTE A (il blob di prima), non patchato
    SB, nB, _ = carica("sim_z43b_B", SIM)         # il CURATO, non patchato
    SC, nC, _ = carica("sim_z43b_C", dst)         # il curato PATCHATO col gancio
    in_conf = _cli_flag.dichiara_configurazione(SB, stampa)
    mis = Misura(SC.CS_M)
    SC._MIS = mis
    stampa("  scena: nmasse=%s sep=%s  ->  n = %d, archi = %d"
           % (getattr(a, "nmasse", "?"), getattr(a, "sep", "?"), nA.n, len(nA.i)))
    stampa("  ### TRE BRACCI: A la PARTE A (blob %s, non patchato), B il CURATO"
           % b0.get("blob_prima"))
    stampa("      (non patchato), C il curato PATCHATO col gancio dei criteri 1 e 5.")
    stampa("      I criteri 2, 3, 4, 6 e 7 confrontano A con B: DUE NON PATCHATI.")
    stampa("      ### E IL PERCHE' L'HA TROVATO IL SIGILLO DELLA PARTE A:")
    stampa("          `_calcpsi_origini` registra <<funzione:NUMERO_DI_RIGA>>, e un")
    stampa("          gancio SPOSTA le righe. Era lo strumento che si misurava addosso.")
    stampa()
    riga("=")
    stampa("IL LOCKSTEP: %d passi, TRE bracci, col BATTITO per passo" % passi)
    riga("=")
    per_passo = []
    mat_prec = vuo_prec = None       # le maschere materia/vuoto del passo PRECEDENTE
    for k in range(1, passi + 1):
        mis.passo = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(SA, nA)
            _passo.passo_pieno(SB, nB)
            _passo.passo_pieno(SC, nC)
        d = confronta_reti(nA, nB)
        rB = getattr(nB, "_r_corrente", None)
        IB = np.abs(np.asarray(nB.psi)[:nB.n]) ** 2
        rec = {"passo": k, "diff": d, "attributi": len(vars(nB)),
               "cs_assente": int(getattr(nB, "_ritmo_cs_assente", 0)),
               "cs_forma": list(getattr(nB, "_ritmo_cs_forma", ()) or ()),
               "chiamate": int(getattr(nB, "_ritmo_chiamate", 0)),
               "n": int(nB.n), "archi": int(len(nB.i))}
        if rB is not None and len(np.atleast_1d(rB)) >= nB.n:
            rr = np.asarray(rB, float)[:nB.n]
            rec["r_mediana"] = float(np.median(rr))
            rec["r_min"] = float(np.min(rr))
            rec["r_max"] = float(np.max(rr))
            rec["r_uguali_a_1"] = int(np.sum(rr == 1.0))
            rec["r_sopra_1"] = int(np.sum(rr > 1.0))
            # ### LA DISTRIBUZIONE, e la SEPARAZIONE chiesta dal guardiano: la parte
            #   UNIFORME di `r` e' un CAMBIO DI UNITA' DI TEMPO -- fisicamente irrilevante,
            #   dice solo di quanto rallenta il passo medio -- e la parte che VARIA fra nodi
            #   e' quella FISICA. Si separano dividendo per la mediana.
            for q in (1, 5, 25, 50, 75, 95, 99):
                rec["r_q%02d" % q] = float(np.quantile(rr, q / 100.0))
            rec["r_media"] = float(np.mean(rr))
            rec["r_std"] = float(np.std(rr))
            med = float(np.median(rr))
            rec["uniforme_r_mediano"] = med          # il cambio di unita' di tempo
            if med > 0.0:
                u = rr / med
                rec["varia_cv"] = float(np.std(rr) / np.mean(rr)) if np.mean(rr) else None
                rec["varia_q95_su_q05"] = (float(np.quantile(u, 0.95))
                                           / float(np.quantile(u, 0.05))
                                           if float(np.quantile(u, 0.05)) > 0 else None)
                rec["varia_max_su_min"] = (float(np.max(u)) / float(np.min(u))
                                           if float(np.min(u)) > 0 else None)
            # ### CRITERIO 4: materia = top 5% di |psi|^2, vuoto = bottom 25%.
            #   `I` di QUESTO passo si accoppia con `r` del passo DOPO (vedi docstring):
            #   qui si salvano entrambi e l'accoppiamento si fa a corsa finita.
            q95 = float(np.quantile(IB, 0.95))
            q25 = float(np.quantile(IB, 0.25))
            rec["soglia_materia_q95"] = q95
            rec["soglia_vuoto_q25"] = q25
            rec["idx_materia"] = int(np.sum(IB >= q95))
            rec["idx_vuoto"] = int(np.sum(IB <= q25))
            # ### L'ACCOPPIAMENTO GIUSTO: `r` di QUESTO passo con le maschere del passo
            #   PRECEDENTE, perche' `r_t = cs_(t-1)/CS_M` e `cs_(t-1)` viene da `I_(t-1)`.
            #   Le maschere si CONSERVANO (due bool per nodo: 3.8 MB su 150 passi), cosi'
            #   non devo dichiarare un limite che si poteva evitare con 4 MB.
            if (mat_prec is not None and len(mat_prec) == len(rr)
                    and bool(np.any(mat_prec)) and bool(np.any(vuo_prec))):
                rec["r_med_materia"] = float(np.median(rr[mat_prec]))
                rec["r_med_vuoto"] = float(np.median(rr[vuo_prec]))
                rec["nodi_materia_prec"] = int(np.sum(mat_prec))
                rec["nodi_vuoto_prec"] = int(np.sum(vuo_prec))
            mat_prec = (IB >= q95)
            vuo_prec = (IB <= q25)
        else:
            rec["r_mediana"] = None
            mat_prec = vuo_prec = None
        per_passo.append(rec)
        print("[battito] passo %d/%d  n=%d archi=%d  diff=%d  r_med=%s  fedelta_diverse=%d"
              % (k, passi, nB.n, len(nB.i), len(d),
                 ("%.6f" % rec["r_mediana"]) if rec.get("r_mediana") is not None else "n/d",
                 mis.diversi), flush=True)

    stampa("  passi girati: %d   n finale: A=%d  B=%d  C=%d   archi: A=%d  B=%d"
           % (passi, nA.n, nB.n, nC.n, len(nA.i), len(nB.i)))
    stampa()

    # ### il criterio 5, A CORSA FINITA, sul braccio C (che ha `I` e `w` catturati)
    riga("=")
    stampa("CRITERIO 5: LOCALITA', MISURATA chiamando LA LEGGE STESSA due volte")
    riga("=")
    if mis.ultimo_I is None:
        loc = {"stato": "NON MISURATO: il gancio di `_cs_nodo` non e' mai scattato"}
    else:
        loc = localita(nC, mis.ultimo_I, mis.ultimo_w, SC.CS_M)
        loc["passo_di_I"] = mis.ultimo_I_passo
    for k in ["stato", "passo_di_I", "n", "uno_su_n", "mean_I", "nodo_perturbato",
              "I_del_nodo", "perturbazione", "contatore_prima", "contatore_dopo",
              "contatore_mosso", "contatore_ripristinato"]:
        if k in loc:
            stampa("  %-28s %s" % (k, loc[k]))
    if loc.get("per_distanza"):
        stampa()
        stampa("  %-10s %-9s %-16s %-16s %s"
               % ("distanza", "nodi", "mediana |dcs|/cs", "max |dcs|/cs", "mediana / (1/n)"))
        for r in loc["per_distanza"]:
            stampa("  %-10d %-9d %-16.6e %-16.6e %.4f"
                   % (r["distanza"], r["nodi"], r["mediana_cambio_rel"],
                      r["max_cambio_rel"], r["rapporto_su_1_su_n"]))
        for k in list(loc):
            if k.startswith("oltre_"):
                r = loc[k]
                stampa("  %-10s %-9d %-16.6e %-16.6e %.4f"
                       % (k.replace("oltre_", ">"), r["nodi"], r["mediana_cambio_rel"],
                          r["max_cambio_rel"], r["rapporto_su_1_su_n"]))
    stampa()

    esito, guasti = rapporto(b0, per_passo, mis, loc, in_conf, nA, nB, passi)
    _scrivi({"braccio0": b0, "esito": esito, "guasti": guasti, "piattaforma": pf,
             "passi": passi, "blob_sim_oggi": blob(SIM), "blob_patch": blob(PATCH),
             "blob_copia": blob(dst), "ancore_patch": fatte,
             "in_configurazione_del_driver": bool(in_conf),
             "soglia_altalena": SOGLIA_ALTALENA, "soglia_autocorr": SOGLIA_AUTOCORR,
             "criterio1_fedelta": {"chiamate": mis.chiamate, "nodi": mis.nodi,
                                   "diversi": mis.diversi,
                                   "chiamate_diverse": mis.chiamate_diverse,
                                   "max_scarto": mis.max_scarto,
                                   "peggiore": mis.peggiore},
             "criterio5_localita": loc,
             "per_passo": [{k: v for k, v in r.items() if not k.startswith("_")}
                           for r in per_passo],
             "a_valle": {"n_A": int(nA.n), "n_B": int(nB.n), "n_C": int(nC.n),
                         "archi_A": int(len(nA.i)), "archi_B": int(len(nB.i))},
             "timbro_strumento": _timbro()})
    return esito


def coppie(pp):
    """-> lista di `{coppia, rapporto, due_lati, esclusa, perche'}`.

    ### La CONVENZIONE: la coppia `(2k-1, 2k)` e' ETICHETTATA DAL PASSO PARI. E' quella del
    guardiano (`b337ec1`), e con un'altra i numeri sarebbero diversi.
    """
    per = {r["passo"]: r for r in pp}
    out = []
    for k in range(1, max(per) // 2 + 1):
        d, e = 2 * k - 1, 2 * k
        if d not in per or e not in per:
            continue
        rd, re_ = per[d].get("r_mediana"), per[e].get("r_mediana")
        rec = {"coppia": e, "passo_dispari": d, "passo_pari": e,
               "r_dispari": rd, "r_pari": re_}
        # ### L'ESCLUSIONE: solo le coppie in cui la cache di cs NON e' allineata.
        #   Si riconosce dal CONTATORE: se e' cresciuto in quel passo, `r = 1` per SICUREZZA.
        pd = per[d]["cs_assente"] - (per.get(d - 1, {"cs_assente": 0})["cs_assente"])
        pe = per[e]["cs_assente"] - per[d]["cs_assente"]
        rec["cache_non_allineata_nel_dispari"] = int(pd)
        rec["cache_non_allineata_nel_pari"] = int(pe)
        if rd is None or re_ is None:
            rec["esclusa"] = True
            rec["perche"] = "r mediano non disponibile"
        elif pd > 0 or pe > 0:
            rec["esclusa"] = True
            rec["perche"] = "la cache di cs NON e' allineata: r = 1 per SICUREZZA, non per legge"
        elif re_ == 0.0:
            rec["esclusa"] = True
            rec["perche"] = "r mediano del passo pari e' ZERO: il rapporto non e' definito"
        else:
            rec["esclusa"] = False
            rec["perche"] = ""
            rec["rapporto"] = rd / re_
            rec["due_lati"] = max(rd / re_, re_ / rd) if rd > 0 else None
        out.append(rec)
    return out


def rapporto(b0, pp, mis, loc, in_conf, nA, nB, passi):
    guasti = []

    riga("=")
    stampa("CRITERIO 1 -- FEDELTA': il r restituito == _cs_nodo_prev / CS_M AL BIT")
    riga("=")
    stampa("  chiamate col ramo di legge: %d   nodi confrontati: %d"
           % (mis.chiamate, mis.nodi))
    stampa("  nodi DIVERSI: %d   chiamate con almeno una differenza: %d"
           % (mis.diversi, mis.chiamate_diverse))
    stampa("  max scarto: %.6e   peggiore: %s" % (mis.max_scarto, mis.peggiore))
    ok1 = (mis.diversi == 0 and mis.chiamate > 0)
    stampa("  ### CRITERIO 1: %s" % ("PASSA" if ok1 else "### FALLISCE"))
    if not ok1:
        guasti.append("criterio 1: fedelta' al bit (diversi=%d, chiamate=%d)"
                      % (mis.diversi, mis.chiamate))
    stampa()

    riga("=")
    stampa("CRITERIO 2 -- NIENTE ALTALENA, PER COPPIA DI PASSI (correzione del guardiano)")
    riga("=")
    cp = coppie(pp)
    escluse = [c for c in cp if c["esclusa"]]
    vive = [c for c in cp if not c["esclusa"]]
    stampa("  coppie totali: %d   ESCLUSE: %d   valutate: %d"
           % (len(cp), len(escluse), len(vive)))
    for c in escluse:
        stampa("      ESCLUSA coppia %-4s  %s" % (c["coppia"], c["perche"]))
    stampa()
    stampa("  LA TABELLA CHIESTA DALLA CORREZIONE (passi %s):"
           % ", ".join(str(x) for x in PASSI_COPPIA))
    stampa("  %-8s %-14s %-14s %-14s %s"
           % ("coppia", "r dispari", "r pari", "rapporto", "due lati"))
    per_et = {c["coppia"]: c for c in cp}
    for k in PASSI_COPPIA:
        c = per_et.get(k)
        if c is None:
            continue
        stampa("  %-8d %-14s %-14s %-14s %s"
               % (k,
                  ("%.6e" % c["r_dispari"]) if c.get("r_dispari") is not None else "n/d",
                  ("%.6e" % c["r_pari"]) if c.get("r_pari") is not None else "n/d",
                  ("%.6f" % c["rapporto"]) if "rapporto" in c else "ESCLUSA",
                  ("%.6f" % c["due_lati"]) if c.get("due_lati") is not None else "n/d"))
    stampa()
    sopra = [c for c in vive if c["coppia"] >= 4 and c["rapporto"] > SOGLIA_ALTALENA]
    valutate_da_3 = [c for c in vive if c["coppia"] >= 4]
    stampa("  coppie dal passo 3 in poi (etichetta >= 4) valutate: %d"
           % len(valutate_da_3))
    stampa("  coppie SOPRA %.1f: %d" % (SOGLIA_ALTALENA, len(sopra)))
    for c in sopra[:20]:
        stampa("      coppia %-4d rapporto %.6f" % (c["coppia"], c["rapporto"]))
    if len(sopra) > 20:
        stampa("      ... e altre %d" % (len(sopra) - 20))
    primo_stabile = None
    for c in sorted(valutate_da_3, key=lambda x: x["coppia"]):
        if all(y["rapporto"] <= SOGLIA_ALTALENA
               for y in valutate_da_3 if y["coppia"] >= c["coppia"]):
            primo_stabile = c["coppia"]
            break
    stampa("  primo passo da cui il rapporto resta <= %.1f: %s"
           % (SOGLIA_ALTALENA, primo_stabile))
    if valutate_da_3:
        mx = max(valutate_da_3, key=lambda x: x["rapporto"])
        stampa("  rapporto MASSIMO fra le coppie valutate: %.6f (coppia %d)"
               % (mx["rapporto"], mx["coppia"]))
        d2 = [c for c in valutate_da_3 if c.get("due_lati") is not None]
        if d2:
            mx2 = max(d2, key=lambda x: x["due_lati"])
            stampa("  ### E A DUE LATI, che il criterio di Luca non vede: max(r, 1/r) = "
                   "%.6f (coppia %d)" % (mx2["due_lati"], mx2["coppia"]))
            stampa("      sopra %.1f a due lati: %d coppie"
                   % (SOGLIA_ALTALENA,
                      len([c for c in d2 if c["due_lati"] > SOGLIA_ALTALENA])))
    # l'AGGREGATO: si riporta, ma NON basta da solo
    med_d = [pp[k]["r_mediana"] for k in range(len(pp))
             if pp[k]["passo"] % 2 == 1 and pp[k].get("r_mediana") is not None]
    med_p = [pp[k]["r_mediana"] for k in range(len(pp))
             if pp[k]["passo"] % 2 == 0 and pp[k].get("r_mediana") is not None]
    agg = (float(np.median(med_d)) / float(np.median(med_p))
           if med_d and med_p and float(np.median(med_p)) != 0.0 else None)
    stampa("  l'AGGREGATO su tutta la corsa: %s   ### si riporta, MA NON BASTA DA SOLO"
           % (("%.6f" % agg) if agg is not None else "n/d"))
    ok2 = (len(sopra) == 0 and len(valutate_da_3) > 0)
    stampa("  ### CRITERIO 2: %s" % ("PASSA" if ok2 else "### FALLISCE"))
    if not ok2:
        guasti.append("criterio 2: %d coppie sopra %.1f dal passo 3"
                      % (len(sopra), SOGLIA_ALTALENA))
    stampa()

    riga("=")
    stampa("CRITERIO 3 -- AUTOCORRELAZIONE A RITARDO 1 della mediana di r")
    riga("=")
    # ### si esclude la coda iniziale in cui la cache non e' allineata: li' r = 1 per
    #   SICUREZZA e una costante non ha autocorrelazione informativa.
    serie, da = [], None
    for r in pp:
        if r.get("r_mediana") is None:
            continue
        pdiff = r["cs_assente"] - (pp[pp.index(r) - 1]["cs_assente"] if pp.index(r) else 0)
        if pdiff > 0:
            serie = []
            da = None
            continue
        if da is None:
            da = r["passo"]
        serie.append(r["r_mediana"])
    ac = None
    if len(serie) >= 4:
        x = np.asarray(serie, float)
        x = x - np.mean(x)
        den = float(np.sum(x * x))
        ac = (float(np.sum(x[:-1] * x[1:]) / den) if den > 0 else None)
    stampa("  serie usata: dal passo %s, %d punti (escluso l'inizio con cache non allineata)"
           % (da, len(serie)))
    stampa("  autocorrelazione a ritardo 1: %s   soglia (LA SCELGO IO): %.2f"
           % (("%.6f" % ac) if ac is not None else "n/d", SOGLIA_AUTOCORR))
    ok3 = (ac is not None and ac >= SOGLIA_AUTOCORR)
    stampa("  ### CRITERIO 3: %s" % ("PASSA" if ok3 else "### FALLISCE"))
    if not ok3:
        guasti.append("criterio 3: autocorrelazione %s sotto %.2f -- L'ANELLO r <-> cs "
                      "OSCILLA" % (ac, SOGLIA_AUTOCORR))
    stampa()

    riga("=")
    stampa("CRITERIO 4 -- SEGNO: r mediano nella MATERIA minore che nel VUOTO")
    riga("=")
    stampa("  ### E' UN CONTROLLO DI FEDELTA', NON UN RISULTATO DI FISICA, e lo correggo qui")
    stampa("      su annotazione del guardiano (2026-10-05): r materia < r vuoto ### SEGUE")
    stampa("      DALLA FORMULA di `_cs_nodo` -- cs_floor = CS_M/(1 + sqrt(I)*sqrt(1/scala))")
    stampa("      DECRESCE in I, e la transizione 0.5*(1 + tanh(1 - u)) pure. ### QUINDI PUO'")
    stampa("      FALLIRE SOLO SE IL CODICE E' SBAGLIATO: e' un FALSO-UNO in attesa, non una")
    stampa("      predizione messa alla prova. ### NON SI RIVENDICA COME CONFERMA DELLA")
    stampa("      FISICA.")
    stampa("  ### L'ACCOPPIAMENTO E' SFASATO DI UNO, E DEVE ESSERLO: r_t = cs_(t-1)/CS_M,")
    stampa("      e cs_(t-1) viene da I_(t-1). Confrontarli nello stesso passo sarebbe")
    stampa("      sfasare la misura del segno. Qui: le MASCHERE materia/vuoto vengono da")
    stampa("      `I` del passo t, e il `r` dal passo t+1. Le maschere si CONSERVANO.")
    stampa()
    stampa("  %-8s %-8s %-16s %-16s %-10s %s"
           % ("r al", "nodi mat", "r mediano MATERIA", "r mediano VUOTO",
              "rapporto", "materia < vuoto"))
    tot, giusti = 0, 0
    for k in range(len(pp)):
        a1 = pp[k]
        rm = a1.get("r_med_materia")
        rv = a1.get("r_med_vuoto")
        if rm is None or rv is None:
            continue
        pdiff = a1["cs_assente"] - (pp[k - 1]["cs_assente"] if k else 0)
        if pdiff > 0:
            continue
        tot += 1
        if rm < rv:
            giusti += 1
        if a1["passo"] in (3, 4, 5, 10, 20, 50, 100, len(pp)):
            stampa("  %-8d %-8d %-16.9f %-16.9f %-10.6f %s"
                   % (a1["passo"], a1.get("nodi_materia_prec", -1), rm, rv,
                      (rm / rv) if rv else float("nan"), "SI" if rm < rv else "### NO"))
    stampa()
    stampa("  passi in cui materia < vuoto: %d su %d   (%s)"
           % (giusti, tot, ("%.2f %%" % (100.0 * giusti / tot)) if tot else "n/d"))
    stampa("  ### CRITERIO 4: si RIPORTA, non ferma. ### ED E' FEDELTA': se NON torna, il")
    stampa("      codice e' sbagliato -- non e' la fisica a smentire un'attesa.")
    stampa()

    riga("=")
    stampa("LA DISTRIBUZIONE DI r, e la SEPARAZIONE fra la parte UNIFORME e quella che VARIA")
    riga("=")
    stampa("  ### ANNOTAZIONE DEL GUARDIANO (2026-10-05), e correggeva una riga FALSA del mio")
    stampa("      task history: <<cs = CS_M -> r = 1 dove la metrica non e' deformata>>.")
    stampa("      ### E' FALSO. Da `_cs_nodo`, cs = CS_M SOLO se I = 0: per ogni I > 0 si ha")
    stampa("      cs_floor = CS_M/(1 + sqrt(I)*sqrt(1/scala)) < CS_M, e la transizione")
    stampa("      0.5*(1 + tanh(1 - u)) vale <= 0.880797 a u = 0 e 0.5 a u = 1 (vuoto")
    stampa("      uniforme). ### QUINDI NESSUN NODO CON CAMPO HA r = 1: il limite r = 1 e'")
    stampa("      L'ASSENZA DI CAMPO, non la metrica non deformata.")
    stampa("  ### E LA SEPARAZIONE CHE CHIEDE: la parte UNIFORME di r e' un CAMBIO DI UNITA'")
    stampa("      DI TEMPO -- fisicamente IRRILEVANTE, dice solo di quanto rallenta il passo")
    stampa("      medio -- e solo la parte che VARIA fra nodi e' FISICA.")
    stampa()
    stampa("  %-6s %-10s %-10s %-10s %-10s %-10s %-10s %s"
           % ("passo", "r q01", "r q25", "r MEDIANO", "r q75", "r q99", "r max", "r > 1"))
    for k in (2, 3, 4, 5, 10, 20, 50, 100, len(pp)):
        if not (1 <= k <= len(pp)):
            continue
        r = pp[k - 1]
        if r.get("r_mediana") is None or "r_q01" not in r:
            continue
        stampa("  %-6d %-10.6f %-10.6f %-10.6f %-10.6f %-10.6f %-10.6f %d"
               % (k, r["r_q01"], r["r_q25"], r["r_q50"], r["r_q75"], r["r_q99"],
                  r["r_max"], r.get("r_sopra_1", -1)))
    stampa()
    stampa("  LA SEPARAZIONE, passo per passo:")
    stampa("  %-6s %-22s %-14s %-14s %s"
           % ("passo", "UNIFORME (r mediano)", "VARIA: CV", "q95/q05", "max/min"))
    for k in (2, 3, 4, 5, 10, 20, 50, 100, len(pp)):
        if not (1 <= k <= len(pp)):
            continue
        r = pp[k - 1]
        if "uniforme_r_mediano" not in r:
            continue
        stampa("  %-6d %-22.9f %-14s %-14s %s"
               % (k, r["uniforme_r_mediano"],
                  ("%.6f" % r["varia_cv"]) if r.get("varia_cv") is not None else "n/d",
                  ("%.6f" % r["varia_q95_su_q05"])
                  if r.get("varia_q95_su_q05") is not None else "n/d",
                  ("%.6f" % r["varia_max_su_min"])
                  if r.get("varia_max_su_min") is not None else "n/d"))
    ult = [r for r in pp if "uniforme_r_mediano" in r]
    if ult:
        u = ult[-1]
        stampa()
        stampa("  ### IL PASSO MEDIO RALLENTA DI UN FATTORE %.6f (al passo %d): e' la parte"
               % (u["uniforme_r_mediano"], u["passo"]))
        stampa("      UNIFORME, cioe' UN CAMBIO DI UNITA' DI TEMPO. ### NON E' FISICA.")
        stampa("  ### LA PARTE FISICA e' la DISPERSIONE: CV = %s, q95/q05 = %s."
               % (("%.6f" % u["varia_cv"]) if u.get("varia_cv") is not None else "n/d",
                  ("%.6f" % u["varia_q95_su_q05"])
                  if u.get("varia_q95_su_q05") is not None else "n/d"))
        stampa("  ### E r > 1 su %d nodi: se non e' ZERO, la forma e' violata."
               % u.get("r_sopra_1", -1))
    stampa()
    riga("=")
    stampa("CRITERIO 6 -- IL CASO CHE DEVE FALLIRE: lo stato DEVE divergere dalla PARTE A")
    riga("=")
    prima_div = None
    for r in pp:
        if r["diff"]:
            prima_div = r["passo"]
            break
    stampa("  primo passo con una differenza: %s" % prima_div)
    stampa("  primi passi in cui la cache di cs NON era allineata (r = 1 per sicurezza):")
    prec = 0
    for r in pp[:8]:
        d = r["cs_assente"] - prec
        prec = r["cs_assente"]
        stampa("      passo %-4d cs_assente +%d (totale %d)  forma %s  r_med %s  r==1 su %s nodi"
               % (r["passo"], d, r["cs_assente"], r["cs_forma"],
                  ("%.6f" % r["r_mediana"]) if r.get("r_mediana") is not None else "n/d",
                  r.get("r_uguali_a_1")))
    for k in (1, 2, 3, 4, 5, 10, 20, 50, 100, len(pp)):
        if 1 <= k <= len(pp):
            d = pp[k - 1]["diff"]
            st = [x for x in d if x["classe"] == "STATO"]
            stampa("  passo %-4d differenze %-5d di cui STATO %-5d" % (k, len(d), len(st)))
    ok6 = (prima_div is not None)
    stampa("  ### CRITERIO 6: %s" % ("PASSA" if ok6 else "### FALLISCE: la cura NON agisce"))
    if not ok6:
        guasti.append("criterio 6: lo stato NON diverge dalla PARTE A")
    stampa()

    riga("=")
    stampa("CRITERIO 7 -- %d PASSI SENZA FERMO, e che cosa cambia A VALLE" % passi)
    riga("=")
    stampa("  passi girati: %d (nessuna eccezione: se ne fosse alzata una non sarei qui)"
           % passi)
    stampa("  n:     A = %-8d B = %-8d  scarto %d" % (nA.n, nB.n, nB.n - nA.n))
    stampa("  archi: A = %-8d B = %-8d  scarto %d"
           % (len(nA.i), len(nB.i), len(nB.i) - len(nA.i)))
    for nome in ("_ritmo_chiamate", "_ritmo_cs_assente", "_cs_lam_degenere",
                 "_cs_in_chiamate", "_cs_in_fallback", "_tum_tetto_colpi",
                 "_tum_tetto_nodi"):
        stampa("  %-22s A = %-14s B = %s"
               % (nome, getattr(nA, nome, "assente"), getattr(nB, nome, "assente")))
    stampa("  ### E DUE CONTATORI DELLA PARTE A SONO SPARITI DA B, e DEVONO:")
    for nome in ("_ritmo_sicurezza", "_ritmo_med_assente", "_ritmo_med_identico",
                 "_ritmo_med_non_promosso", "_ritmo_f_tutto_nullo",
                 "_ritmo_med_sul_pavimento", "_med_f_prec", "_med_f_ultimo"):
        stampa("      %-26s A = %-16s B = %s"
               % (nome, getattr(nA, nome, "assente"), getattr(nB, nome, "assente")))
    stampa()

    riga("=")
    stampa("IL VERDETTO")
    riga("=")
    stampa("  configurazione del driver dichiarata INTERA sul braccio B (il CURATO): %s"
           % bool(in_conf))
    stampa("  criterio 0 (braccio 0):            %s"
           % ("PASSA" if b0.get("coincide") else "### FALLISCE"))
    stampa("  criterio 1 (fedelta' al bit):      %s" % ("PASSA" if ok1 else "### FALLISCE"))
    stampa("  criterio 2 (altalena per coppia):  %s" % ("PASSA" if ok2 else "### FALLISCE"))
    stampa("  criterio 3 (autocorrelazione):     %s" % ("PASSA" if ok3 else "### FALLISCE"))
    stampa("  criterio 4 (segno): FEDELTA', non fisica  SI RIPORTA (%d su %d)"
           % (giusti, tot))
    stampa("  criterio 5 (localita'):            SI RIPORTA (%s)" % loc.get("stato"))
    stampa("  criterio 6 (deve divergere):       %s" % ("PASSA" if ok6 else "### FALLISCE"))
    stampa("  criterio 7 (%d passi):            PASSA" % passi)
    if guasti:
        stampa()
        stampa("  ### FERMO. I GUASTI:")
        for g in guasti:
            stampa("      - " + g)
        return 1, guasti
    stampa()
    stampa("  ### TUTTI I CRITERI CHE FERMANO PASSANO.")
    return 0, []


# =============================================================== IL COLLAUDO
# ### GLI STRUMENTI DI QUESTO REPO HANNO SBAGLIATO TRE VOLTE IN UN GIORNO, e ogni volta
#   l'ha trovato la CORSA, non io. Quindi: ogni funzione di calcolo si collauda su casi a
#   RISPOSTA NOTA, e fra i casi ce ne sono che DEVONO FALLIRE.

def _finto(n, i, j):
    class N(object):
        pass
    o = N()
    o.n = n
    o.i = np.asarray(i)
    o.j = np.asarray(j)
    return o


def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        print("  %-6s %-58s %s" % ("OK" if ok else "### KO", nome, dett))

    # --- 1. la CONVENZIONE della coppia: (2k-1, 2k) etichettata dal PARI
    pp = [{"passo": k, "r_mediana": (2.0 if k % 2 else 1.0), "cs_assente": 0}
          for k in range(1, 11)]
    cp = coppie(pp)
    prova("coppie: la coppia e' etichettata dal passo PARI",
          [c["coppia"] for c in cp] == [2, 4, 6, 8, 10],
          str([c["coppia"] for c in cp]))
    prova("coppie: alternanza 2/1 -> rapporto 2.0 ESATTO",
          all(abs(c["rapporto"] - 2.0) < 1e-15 for c in cp),
          "%.17g" % cp[0]["rapporto"])
    prova("coppie: il DUE LATI su 2/1 vale 2.0",
          all(abs(c["due_lati"] - 2.0) < 1e-15 for c in cp))

    # --- 2. IL CASO ROVESCIATO, che il criterio a UN lato NON vede
    pr = [{"passo": k, "r_mediana": (1.0 if k % 2 else 2.0), "cs_assente": 0}
          for k in range(1, 11)]
    cr = coppie(pr)
    prova("coppie: alternanza ROVESCIATA -> rapporto 0.5, il criterio a un lato PASSA",
          all(abs(c["rapporto"] - 0.5) < 1e-15 for c in cr),
          "%.17g" % cr[0]["rapporto"])
    prova("coppie: ... ma il DUE LATI la VEDE: 2.0",
          all(abs(c["due_lati"] - 2.0) < 1e-15 for c in cr))

    # --- 3. L'ESCLUSIONE: una coppia con la cache non allineata ESCE, e si CONTA
    pe = [{"passo": k, "r_mediana": 1.0, "cs_assente": (1 if k >= 3 else 0)}
          for k in range(1, 9)]
    ce = coppie(pe)
    esc = [c["coppia"] for c in ce if c["esclusa"]]
    prova("coppie: la coppia col contatore CRESCIUTO e' ESCLUSA, le altre no",
          esc == [4], "escluse: %s" % esc)
    prova("coppie: e l'esclusione dice PERCHE'",
          all(c["perche"] for c in ce if c["esclusa"]))

    # --- 4. autocorrelazione: alternanza perfetta -> -1, monotona -> ~+1
    def ac(serie):
        x = np.asarray(serie, float)
        x = x - np.mean(x)
        d = float(np.sum(x * x))
        return float(np.sum(x[:-1] * x[1:]) / d) if d > 0 else None
    alt = [1.0, 2.0] * 20
    prova("autocorr: alternanza perfetta a periodo 2 -> circa -1",
          ac(alt) < -0.9, "%.6f" % ac(alt))
    prova("autocorr: serie monotona -> positiva",
          ac(list(range(40))) > 0.9, "%.6f" % ac(list(range(40))))
    prova("autocorr: la SOGLIA che ho scelto BOCCIA l'alternanza",
          ac(alt) < SOGLIA_AUTOCORR, "%.6f < %.2f" % (ac(alt), SOGLIA_AUTOCORR))

    # --- 5. distanze: una CATENA 0-1-2-3-4 da' 0,1,2,3,4
    cat = _finto(5, [0, 1, 2, 3], [1, 2, 3, 4])
    d = distanze(cat, 0, 6)
    prova("distanze: su una catena da' 0,1,2,3,4", list(d) == [0, 1, 2, 3, 4], str(list(d)))
    d2 = distanze(cat, 0, 2)
    prova("distanze: col tetto a 2 salti i lontani restano -1",
          list(d2) == [0, 1, 2, -1, -1], str(list(d2)))
    iso = _finto(3, [0], [1])
    prova("distanze: un nodo NON connesso resta -1",
          list(distanze(iso, 0, 5)) == [0, 1, -1], str(list(distanze(iso, 0, 5))))

    # --- 6. localita': il PRE-CONTROLLO salta, e il contatore NON si muove
    class FintaRete(object):
        def __init__(self, n):
            self.n = n
            self.i = np.asarray([0, 1])
            self.j = np.asarray([1, 2])
            self.chiamate = 0

        def _cs_nodo(self, I, w):
            self.chiamate += 1
            self._cs_lam_degenere = getattr(self, "_cs_lam_degenere", 0) + 1
            return np.full(self.n, 2.0) - np.asarray(I, float)[:self.n] * 1e-3

    fr = FintaRete(3)
    out = localita(fr, np.zeros(3), np.ones(2), 2.0, salti=3)
    prova("localita': mean(I) = 0 -> SALTATO, la legge NON viene chiamata",
          out["stato"].startswith("SALTATO") and fr.chiamate == 0,
          "chiamate: %d" % fr.chiamate)
    prova("localita': e il contatore NON esiste nemmeno",
          not hasattr(fr, "_cs_lam_degenere"))

    # --- 7. localita': il contatore si RIPRISTINA anche quando la legge lo muove
    fr2 = FintaRete(3)
    out2 = localita(fr2, np.asarray([1.0, 2.0, 3.0]), np.ones(2), 2.0, salti=3)
    prova("localita': la legge e' chiamata DUE volte, una per stato",
          fr2.chiamate == 2, "chiamate: %d" % fr2.chiamate)
    prova("localita': il contatore si e' MOSSO, e lo DICHIARA",
          out2.get("contatore_mosso") is True, str(out2.get("contatore_mosso")))
    prova("localita': ### ED E' STATO RIPRISTINATO al valore di prima",
          out2.get("contatore_ripristinato") == out2.get("contatore_prima"),
          "prima=%s dopo il ripristino=%s"
          % (out2.get("contatore_prima"), out2.get("contatore_ripristinato")))
    prova("localita': riporta per DISTANZA, non un numero solo",
          len(out2.get("per_distanza", [])) >= 2,
          "%d righe" % len(out2.get("per_distanza", [])))

    # --- 8. il comparatore: inf contro inf NON deve ALZARE (il difetto di MEM_FASE)
    with np.errstate(all="raise"):
        a = np.asarray([np.inf, 1.0, np.nan])
        b = np.asarray([np.inf, 2.0, np.nan])
        try:
            ug, nd, nota, mx = confronta(a, b)
            alzato = False
        except Exception as e:
            ug = nd = nota = mx = None
            alzato = repr(e)
    prova("confronta: inf contro inf e NaN contro NaN NON alzano", alzato is False,
          str(alzato))
    prova("confronta: inf==inf e NaN==NaN sono UGUALI, 1 sola cella diversa",
          nd == 1, "nd=%s" % nd)
    prova("confronta: lo scarto si misura SOLO sul finito", mx == 1.0, "mx=%s" % mx)

    # --- 9. classe(): i contatori nuovi sono CONTATORI, non stato
    prova("classe: `_ritmo_cs_assente` e' un contatore",
          classe("_ritmo_cs_assente") == "contatore/registro")
    prova("classe: `_ritmo_cs_forma` e' un contatore",
          classe("_ritmo_cs_forma") == "contatore/registro")
    prova("classe: `psi` e' STATO", classe("psi") == "STATO")

    riga("=")
    ko = [n for n, o, _d in esiti if not o]
    stampa("COLLAUDO: %d su %d" % (len(esiti) - len(ko), len(esiti)))
    if ko:
        stampa("### FALLITI:")
        for n in ko:
            stampa("    - " + n)
    riga("=")
    return 1 if ko else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
