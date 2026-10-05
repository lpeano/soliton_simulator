# -*- coding: utf-8 -*-
"""IL SIGILLO DI `Z43` CURA (1): `r` va UNA VOLTA SOLA, e nella FREQUENZA no.

*(Decisione di Luca del 2026-10-05. I **sei criteri** sono fissati in
`doc/TASK_HISTORY/2026-10-05_z43-cura1-orologio-r-una-volta.md`, committato **prima** in
`45e7130`.)*

### I SEI CRITERI
| | che cosa pretende | e se fallisce |
|---|---|---|
| **`0`** | **braccio 0**: il *prima* + la patch committata = **il blob di oggi**, al byte | ### **FERMO** |
| **`1`** | ### **IDENTITA' AL BYTE nei passi 1 e 2** *(lockstep su `vars(net)` INTERO)*: li' `r = 1` **esatto per costruzione** | ### ⛔ **la patch tocca altro: FERMO** |
| **`2`** | ### **CASO CHE DEVE FALLIRE: dal passo 3 lo stato DEVE divergere** | ### ⛔ **la cura non agisce: FERMO** |
| **`3`** | **`STEP2` intatto**: `omega_clk == coerenza * (cs_prec/CS_M)**2` ### **al bit**, su ogni nodo e ogni passo | ### **FERMO** |
| **`4`** | **l'altalena sparisce**: lo misura lo **strumento di `Z43`** *(`7b71aa48`)*, rigirato sul blob nuovo. ### **NON lo fa questo sigillo** | — |
| **`5`** | **`150` passi senza `FERMO` di invarianti**, e che cosa cambia **a valle**, ### **riportato e non giudicato** | ### **FERMO** |

### ⛔ **PERCHE' IL CRITERIO `3` NON E' UNA DIVISIONE**
`omega_clk / coerenza == (cs/CS_M)**2` ### **non si puo' chiedere al bit:** in IEEE
`(a*b)/a != b` in generale. ### **Quindi si verifica la MOLTIPLICAZIONE, nello stesso
ordine in cui la legge la scrive:** `omega_clk == coerenza * (_csn2/CS_M)**2`.
### **Chiedere la divisione sarebbe un FALSO-ZERO garantito dall'aritmetica.**

### ⚠ **E IL RAMO LEGACY NON E' MISURABILE GIRANDO:** `DEPARAM_OROLOGIO` e' `True`, quindi
`:5982` ### **non viene eseguito.** La sua cura e' verificabile **solo dall'AST e dalla
lettura**, e il sigillo ### **lo DICHIARA invece di tacerlo.**

# ESENTE-H-P8: le occorrenze di `HEAD` in questo file stanno nella DOCSTRING di `braccio0()`
#   e dicono il CONTRARIO di cio' che il presidio teme: spiegano perche' il *prima* NON si
#   prende da `HEAD~1` ma dal PADRE DEL COMMIT CHE HA CAMBIATO IL SIMULATORE. Potevo
#   scrivere `@~1`, che passa il controllo: NON LO FACCIO -- sarebbe disarmare un presidio
#   cambiando le parole. E' la TERZA volta per la stessa ragione.
# ESENTE-H-P3: la COPIA PATCHATA serve al criterio 3, perche' `omega_clk`, la coerenza
#   d'arco e `_csn2` vivono SOLO dentro `_passo_spinoriale`: ricostruirli fuori sarebbe una
#   SECONDA scrittura della stessa legge (`9-ter`). La scena passa TUTTA dal CLI, e la
#   configurazione INTERA si DICHIARA.
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
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_z43_cura1")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PATCH = os.path.join(RADICE, "csv", "_seal_fork", "_z43_cura1_patch.py")
PASSI = 150

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


# =============================================================== IL COMPARATORE
# ### ⚠ TERZA COPIA dello stesso comparatore, e LO DICHIARO: e' la voce
#   `SIGILLO-COMPARATORE-DUPLICATO`, ora con TRE copie invece di due. La cura giusta e'
#   estrarlo in un modulo comune, e NON si fa dentro il lavoro di un altro mandato.
#   ### QUI PORTO LA LEZIONE IMPARATA: lo scarto si misura SOLO sulle celle FINITE, perche'
#   `inf - inf` ALZA (il simulatore mette `np.seterr` a raise) -- ed e' il difetto che ha
#   ucciso il sigillo di `MEM_FASE` al passo 61.

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
            nota = ("" if not nonfin
                    else "%d celle diverse NON FINITE" % nonfin)
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
            or nome in ("_veleno_registro",):
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


# =============================================================== LA COPIA, per il criterio 3
def copia_patchata():
    """Una COPIA del sorgente CURATO con UN punto di verifica dentro `_passo_spinoriale`.

    ### `omega_clk`, la coerenza d'arco e `_csn2` vivono SOLO li': ricostruirli fuori
    ### sarebbe una SECONDA scrittura della stessa legge (`9-ter`).
    """
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    dst = os.path.join(FUORI, "_sim_step2.py")
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
        + "_MIS = None   # [SIGILLO Z43 CURA 1] lo riempie lo strumento" + NL,
        "il gancio di modulo `_MIS`")
    # ### il punto di verifica: SUBITO DOPO che `STEP2` ha moltiplicato per (cs/CS_M)^2.
    uno("                    omega_clk = omega_clk * (_csn2 / CS_M) ** 2" + NL,
        "                    _coer_pre = omega_clk" + NL
        + "                    omega_clk = omega_clk * (_csn2 / CS_M) ** 2" + NL
        + "                    if _MIS is not None:" + NL
        + "                        _MIS(self, coer=_coer_pre, csn2=_csn2," + NL
        + "                             omega_clk=omega_clk)" + NL,
        "il punto di verifica di `STEP2`, dopo la moltiplicazione")
    io.open(dst, "w", encoding="utf-8", newline=NL).write(t)
    return dst, fatte


class Step2(object):
    """`CRITERIO 3`: `omega_clk == coerenza * (cs_prec/CS_M)**2` AL BIT."""

    def __init__(self, CS_M):
        self.CS_M = float(CS_M)
        self.chiamate = 0
        self.nodi = 0
        self.diversi = 0
        self.chiamate_diverse = 0
        self.max_scarto = 0.0
        self.peggiore = None
        self.passo = 0

    def __call__(self, net, coer, csn2, omega_clk):
        self.chiamate += 1
        c = np.asarray(coer, float)
        cs = np.asarray(csn2, float)
        o = np.asarray(omega_clk, float)
        # ### LO STESSO ORDINE DELLA LEGGE: `coer * (cs/CS_M)**2`, non `o/c`.
        atteso = c * (cs / self.CS_M) ** 2
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


# =============================================================== BRACCIO 0
def braccio0():
    """### IL *PRIMA* VIENE DAL PADRE DEL COMMIT CHE HA CAMBIATO IL SIMULATORE.

    ### ⛔ **NON `HEAD~1`:** dopo il commit della cura ne arriva un altro, e `HEAD~1`
    diventa **il commit della cura** -- il *prima* estratto sarebbe ### **GIA' CURATO.**
    Lo trovo' il sigillo di `VELENO-ARCHI-KEEP` rifiutandosi di proseguire *(`c7f2eb3`)*.
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


def main(argv):
    passi = PASSI
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    riga("=")
    stampa("IL SIGILLO DI Z43 CURA (1): `r` va UNA VOLTA SOLA, e nella FREQUENZA no")
    riga("=")
    stampa()
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa("  simulatore OGGI %s   patch %s" % (blob(SIM)[:8], blob(PATCH)[:8]))
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
    if vecchio is None:
        stampa("### IL BRACCIO 0 NON SI E' POTUTO RICOSTRUIRE. MI FERMO.")
        _scrivi({"braccio0": b0, "esito": 1, "piattaforma": pf})
        return 1

    # --- la copia patchata per il criterio 3
    dst, fatte = copia_patchata()
    stampa("  copia patchata per il criterio 3: %s  blob %s  (%d ancore)"
           % (os.path.basename(dst), blob(dst)[:8], len(fatte)))
    for f in fatte:
        stampa("      - " + f)
    stampa()

    # ### ⛔ TRE BRACCI, E LA RAGIONE L HA TROVATA IL PRIMO GIRO DI QUESTO SIGILLO:
    #   con DUE bracci (vecchio NON patchato contro curato PATCHATO) il criterio 1 dava
    #   1 differenza ai passi 1 e 2, su `_calcpsi_origini`, con la nota <<chiavi diverse>>.
    #   ### NON ERA LA CURA: `_calcpsi_origini` e' un dizionario che registra
    #   ### **"nome_funzione:NUMERO_DI_RIGA"** di chi chiama `calcola_psi()` senza `w`
    #   (`:6271-6279`). Il mio gancio aggiunge QUATTRO righe, quindi i numeri di riga dei
    #   chiamanti SI SPOSTANO e le chiavi differiscono -- ### PER COSTRUZIONE.
    #   ⚠ E L HO VERIFICATO IN MODO INDIPENDENTE prima di cambiare lo strumento: due passi,
    #   vecchio contro curato SENZA gancio, ### ZERO differenze su tutti gli attributi.
    # ➜ LA FORMA GIUSTA: i criteri 1, 2 e 5 confrontano DUE SORGENTI NON PATCHATI (`A` il
    #   vecchio, `B` il curato), e il criterio 3 gira su un TERZO braccio `C`, il curato
    #   PATCHATO col gancio. ### Cosi' nessun criterio confronta un patchato con un
    #   ### non-patchato, e il registro delle righe non puo' mentire.
    SA, nA, a = carica("sim_z43_A", vecchio)      # il blob VECCHIO, NON patchato
    SB, nB, _ = carica("sim_z43_B", SIM)          # il CURATO, NON patchato
    SC, nC, _ = carica("sim_z43_C", dst)          # il CURATO, patchato col gancio
    in_conf = _cli_flag.dichiara_configurazione(SB, stampa)
    st2 = Step2(SC.CS_M)
    SC._MIS = st2
    stampa("  scena: nmasse=%s sep=%s  ->  n = %d, archi = %d"
           % (getattr(a, "nmasse", "?"), getattr(a, "sep", "?"), nA.n, len(nA.i)))
    stampa("  ### TRE BRACCI: A il VECCHIO (non patchato), B il CURATO (non")
    stampa("      patchato), C il curato PATCHATO col gancio del criterio 3.")
    stampa("      I criteri 1, 2 e 5 confrontano A con B: DUE NON PATCHATI.")
    stampa("      ### E IL PERCHE' L'HA TROVATO IL PRIMO GIRO: con A non patchato e")
    stampa("          B patchato, `_calcpsi_origini` differiva ai passi 1-2 --")
    stampa("          e' un dizionario che registra <<funzione:NUMERO_DI_RIGA>> di")
    stampa("          chi chiama calcola_psi (:6271-6279), e il gancio sposta le")
    stampa("          righe. NON era la cura: era lo strumento che si misurava")
    stampa("          addosso.")
    stampa("  ### E IL RAMO LEGACY NON E' MISURABILE GIRANDO: DEPARAM_OROLOGIO = %s,"
           % getattr(SB, "DEPARAM_OROLOGIO", "?"))
    stampa("      quindi `:5982` NON viene eseguito. La sua cura e' verificabile solo")
    stampa("      dall'AST e dalla lettura, NON da un numero. LO DICHIARO.")
    stampa()
    riga("=")
    stampa("IL LOCKSTEP: %d passi, DUE bracci, col BATTITO per passo" % passi)
    riga("=")
    per_passo = []
    for k in range(1, passi + 1):
        st2.passo = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(SA, nA)
            _passo.passo_pieno(SB, nB)
            _passo.passo_pieno(SC, nC)
        d = confronta_reti(nA, nB)
        per_passo.append({"passo": k, "diff": d, "attributi": len(vars(nB))})
        print("[battito] passo %d/%d  n=%d archi=%d  diff=%d  step2_diversi=%d"
              % (k, passi, nB.n, len(nB.i), len(d), st2.diversi), flush=True)
    stampa("  passi girati: %d   n finale: A=%d  B=%d   archi: A=%d  B=%d"
           % (passi, nA.n, nB.n, len(nA.i), len(nB.i)))
    stampa()

    esito, guasti = rapporto(b0, per_passo, st2, in_conf, nA, nB, passi)
    _scrivi({"braccio0": b0, "esito": esito, "guasti": guasti, "piattaforma": pf,
             "passi": passi, "blob_sim_oggi": blob(SIM), "blob_patch": blob(PATCH),
             "blob_copia": blob(dst), "ancore_patch": fatte,
             "in_configurazione_del_driver": bool(in_conf),
             "attributi_per_passo": per_passo[0]["attributi"] if per_passo else 0,
             "per_passo": per_passo,
             "criterio3_step2": {"chiamate": st2.chiamate, "nodi": st2.nodi,
                                 "diversi": st2.diversi,
                                 "chiamate_diverse": st2.chiamate_diverse,
                                 "max_scarto": st2.max_scarto,
                                 "peggiore": st2.peggiore},
             "a_valle": {"n_A": int(nA.n), "n_B": int(nB.n), "n_C": int(nC.n),
                         "archi_A": int(len(nA.i)), "archi_B": int(len(nB.i))},
             "timbro_strumento": _timbro()})
    return esito


def rapporto(b0, pp, st2, in_conf, nA, nB, passi):
    riga("=")
    stampa("CRITERIO 1: IDENTITA' AL BYTE ai passi 1 e 2 (li' r = 1 ESATTO)")
    riga("=")
    for k in (1, 2):
        if len(pp) >= k:
            d = pp[k - 1]["diff"]
            stampa("  passo %d: differenze %d   (attributi per passo: %d)"
                   % (k, len(d), pp[k - 1]["attributi"]))
            for x in d:
                stampa("      %-26s %-20s quanti=%-10s max_scarto=%s  %s"
                       % (x["nome"], x["classe"], x["quanti"],
                          ("%.6e" % x["max_scarto"])
                          if x["max_scarto"] is not None else "n/d", x["nota"]))
    stampa()
    riga("=")
    stampa("CRITERIO 2 -- IL CASO CHE DEVE FALLIRE: dal passo 3 lo stato DEVE divergere")
    riga("=")
    prima_div = None
    for r in pp:
        if r["diff"]:
            prima_div = r["passo"]
            break
    stampa("  primo passo con una differenza: %s" % prima_div)
    for k in (3, 4, 5, 10, 20, 50, 100, len(pp)):
        if 1 <= k <= len(pp):
            stampa("      passo %-5d differenze %d" % (k, len(pp[k - 1]["diff"])))
    stampa()
    riga("=")
    stampa("CRITERIO 3: STEP2 intatto -- omega_clk == coerenza * (cs_prec/CS_M)**2 AL BIT")
    riga("=")
    stampa("  chiamate verificate: %d   nodi confrontati: %d"
           % (st2.chiamate, st2.nodi))
    stampa("  nodi DIVERSI: %d   chiamate con differenze: %d   max scarto: %.3e"
           % (st2.diversi, st2.chiamate_diverse, st2.max_scarto))
    if st2.peggiore:
        stampa("  il peggiore: %s" % (st2.peggiore,))
    stampa("  ### NON E' UNA DIVISIONE: in IEEE (a*b)/a != b, quindi si verifica LA")
    stampa("      MOLTIPLICAZIONE nello stesso ordine della legge. Chiedere la divisione")
    stampa("      sarebbe un FALSO-ZERO garantito dall'aritmetica.")
    stampa()
    riga("=")
    stampa("CRITERIO 5: 150 passi, e CHE COSA CAMBIA A VALLE (riportato, non giudicato)")
    riga("=")
    stampa("  passi girati: %d   SENZA eccezioni di invarianti: %s" % (len(pp), len(pp) == passi))
    stampa("      %-22s %-14s %-14s" % ("", "A (vecchio)", "B (curato)"))
    stampa("      %-22s %-14d %-14d" % ("n finale", nA.n, nB.n))
    stampa("      %-22s %-14d %-14d" % ("archi finali", len(nA.i), len(nB.i)))
    for et, k in [("divisioni", "_g_div_tot"), ("Schwinger", "_g_sch_tot"),
                  ("nascite", "_g_nascita_tot")]:
        va, vb = getattr(nA, k, None), getattr(nB, k, None)
        if va is not None or vb is not None:
            stampa("      %-22s %-14s %-14s" % (et, va, vb))
    stampa()
    stampa("  ### IL CRITERIO 4 (l'altalena) NON LO FA QUESTO SIGILLO: lo misura lo")
    stampa("      strumento di Z43 (7b71aa48), rigirato sul blob nuovo. E' una corsa a se'.")
    stampa()
    guasti = []
    if not b0.get("coincide"):
        guasti.append("braccio 0: la patch NON ridA' il blob di oggi")
    if not pp:
        guasti.append("zero passi: zero NON e' un'identita'")
    else:
        for k in (1, 2):
            if len(pp) >= k and pp[k - 1]["diff"]:
                guasti.append("CRITERIO 1: al passo %d ci sono %d differenze: la patch "
                              "tocca ALTRO" % (k, len(pp[k - 1]["diff"])))
        if prima_div is None:
            guasti.append("CRITERIO 2 (il caso che DEVE fallire): lo stato NON diverge MAI "
                          "-- la cura non agisce")
        elif prima_div < 3:
            guasti.append("CRITERIO 2: la prima divergenza e' al passo %d, PRIMA del 3"
                          % prima_div)
    if st2.chiamate == 0:
        guasti.append("CRITERIO 3: zero chiamate verificate -- zero NON e' un'identita'")
    if st2.diversi:
        guasti.append("CRITERIO 3: STEP2 NON e' intatto -- %d nodi diversi, max scarto %.3e"
                      % (st2.diversi, st2.max_scarto))
    if len(pp) != passi:
        guasti.append("CRITERIO 5: la corsa si e' fermata al passo %d su %d"
                      % (len(pp), passi))
    if not in_conf:
        guasti.append("la configurazione NON e' quella del driver")
    riga("=")
    stampa("L'ESITO")
    riga("=")
    if guasti:
        stampa("  ### IL SIGILLO NON PASSA, e mi FERMO. Che cosa non torna:")
        for g in guasti:
            stampa("      - " + g)
        stampa("  ### NON AMMORBIDISCO I CRITERI: erano fissati PRIMA, in 45e7130.")
        riga("=")
        return 1, guasti
    stampa("  ### I CINQUE CRITERI DI QUESTO SIGILLO PASSANO:")
    stampa("      0: la patch su %s ridA' %s AL BYTE" % (b0["blob_prima"], b0["blob_oggi"]))
    stampa("      1: ZERO differenze ai passi 1 e 2")
    stampa("      2: la prima divergenza e' al passo %d -- la cura AGISCE" % prima_div)
    stampa("      3: STEP2 intatto su %d nodi in %d chiamate" % (st2.nodi, st2.chiamate))
    stampa("      5: %d passi girati, e il valle e' riportato sopra" % len(pp))
    stampa("  ### E IL CRITERIO 4 RESTA DA MISURARE con lo strumento di Z43.")
    riga("=")
    return 0, []


def _timbro():
    t = getattr(_presidio, "timbro", None)
    if t is None:
        return {"nota": "il presidio non espone `timbro`"}
    try:
        d = t(__file__)
        return d if isinstance(d, dict) else {"timbro": str(d)}
    except Exception as e:
        return {"nota": "timbro non leggibile: %r" % (e,)}


def _scrivi(d):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    jp = os.path.join(FUORI, "_sigillo.json")
    io.open(jp, "w", encoding="utf-8", newline=NL).write(
        json.dumps(d, indent=1, sort_keys=True, default=str))
    stampa("scritto: " + jp)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
