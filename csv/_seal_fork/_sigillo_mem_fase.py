# -*- coding: utf-8 -*-
"""IL SIGILLO DELLA CURA (2) DI `MEM-HEBB-VERSO`: il flag `MEM_FASE`.

*(Decisione di Luca del 2026-10-04, confermata dal referto `2717308`. I cinque criteri sono
fissati in `doc/TASK_HISTORY/2026-10-05_mem-hebb-verso-cura2-fase.md`, committato **prima**
in `634762c`.)*

### I CINQUE CRITERI, e TRE BRACCI in lockstep
| | che cosa pretende | e se fallisce |
|---|---|---|
| **`0`** | **braccio 0**: il *prima* + la patch committata = **il blob di oggi**, al byte | ### **FERMO** |
| **`1`** | **`A`** *(il blob VECCHIO)* contro **`B`** *(il nuovo con `MEM_FASE = True`)*: ### **identita' AL BYTE** su `150` passi, su **TUTTI** gli attributi di `net` | ### **il flag non e' inerte da acceso: FERMO** |
| **`2`** | **`B`** contro **`C`** *(il nuovo col DEFAULT, `MEM_FASE = False`)*, ### **al PASSO 1**: le differenze ### **SOLO in `phi`** | ### ⛔ **se differisce altro: FERMO** |
| **`3`** | ### **CASO CHE DEVE FALLIRE:** al passo 1 `phi` ### **DEVE** differire | ### ⛔ **lo spegnimento non spegne niente: FERMO** |
| **`4`** | dal passo **2**: la **crescita** delle differenze per attributo, ### **senza giudicarla** | — |

### ⛔ **PERCHE' TRE BRACCI E NON DUE:** il criterio `1` confronta col **blob vecchio**
*(che non ha il flag)*, il criterio `2` confronta ### **i due stati del flag NELLO STESSO
BLOB.** Con due bracci uno dei due confronti sarebbe stato **fra cose diverse per due
ragioni insieme** *(blob diverso **e** flag diverso)*, e ### **non si saprebbe a quale
attribuire una differenza.**

### ⚠ **E IL CRITERIO `2` POGGIA SU UNA CATENA CENSITA DALL'AST**, scritta nel task history:
`:9578` e' l'### **unica** scrittura di `phi` nella funzione **e** l'### **ultima scrittura
di stato**; `memoria_hebbiana_moto` e' l'### **ultima legge** della composizione; e il freno
su `d0`, che gira dopo, ### **non legge `phi`.**
### **Se al passo 1 differisse altro, la prima cosa da rivedere e' QUELLA LETTURA.**

# ESENTE-H-P8: le DUE occorrenze di `HEAD` in questo file stanno nella DOCSTRING di
#   `braccio0()`, e dicono ESATTAMENTE IL CONTRARIO di cio' che il presidio teme: spiegano
#   perche' il *prima* NON si prende da `HEAD~1` ma dal PADRE DEL COMMIT CHE HA CAMBIATO IL
#   SIMULATORE. Il hook cerca la sottostringa `HEAD`, e la trova nella prosa.
#   ⛔ POTEVO SCRIVERE `@~1`, che in git e' lo stesso e passa il controllo. NON LO FACCIO:
#   sarebbe DISARMARE UN PRESIDIO CAMBIANDO LE PAROLE, ed e' l'errore che H-FILE ha fatto su
#   se stesso il 2026-10-04. E' la SECONDA volta che dichiaro questa esenzione per la stessa
#   ragione (la prima e' `_sigillo_veleno_keep.py`, 92ecb04): il codice e' GIUSTO, e il
#   braccio 0 lo VERIFICA -- se il *prima* fosse sbagliato, il blob non tornerebbe.
# ESENTE-H-P3: il flag `MEM_FASE` NON HA un'opzione da riga di comando, di proposito
#   (`README.md` par. 9-bis: «si impostano SUL MODULO da uno script di rigiocata ... non
#   devono poter essere accese per sbaglio da un comando»), come `MEM_MOTO` e
#   `MEM_MOTO_TUTTO`. Quindi impostarlo sul modulo E' il modo prescritto, non un aggiramento
#   del CLI. La SCENA passa TUTTA dal CLI, e la configurazione INTERA si DICHIARA.
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
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_mem_fase")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PATCH = os.path.join(RADICE, "csv", "_seal_fork", "_mem_fase_patch.py")
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
# ### ⚠ QUESTO COMPARATORE E' UNA SECONDA COPIA di quello di
#   `csv/_seal_fork/_sigillo_veleno_keep.py` (`ee1df224`), e LO DICHIARO invece di
#   nasconderlo: due copie possono divergere, ed e' la stessa obiezione che `9-ter` fa
#   alle leggi. ### LA CURA GIUSTA e' estrarlo in un modulo comune, e NON la faccio ora
#   per il CONGELAMENTO DELL'INFRASTRUTTURA (decisione di Luca del 2026-10-04).
#   ### VA IN CODA, come `SIGILLO-COMPARATORE-DUPLICATO`.

def _vettori_di(v):
    """Gli array che DEFINISCONO un oggetto non-`ndarray`, o `None`.

    ### `_S` e' una `csr_matrix` (l'ADIACENZA, cioe' STATO vero) e `rng` e' un
    ### `Generator`: se i flussi casuali divergessero, le traiettorie divergerebbero
    ### **per quello e non per la cura.** Un sigillo che li dichiara <<non
    ### confrontabili>> non sta sigillando.
    """
    if hasattr(v, "bit_generator"):
        return ("rng", v.bit_generator.state)
    if all(hasattr(v, k) for k in ("data", "indices", "indptr", "shape")):
        return ("sparsa", (tuple(v.shape), np.asarray(v.data),
                           np.asarray(v.indices), np.asarray(v.indptr)))
    return None


def _stato_rng_uguale(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return set(a) == set(b) and all(_stato_rng_uguale(a[k], b[k]) for k in a)
    if isinstance(a, np.ndarray):
        return bool(a.shape == b.shape and np.array_equal(a, b))
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(_stato_rng_uguale(x, y) for x, y in zip(a, b))
    return bool(a == b)


def confronta(x, y):
    """-> `(uguale, quanti_diversi, nota, max_scarto)`. `NaN` contro `NaN` e' UGUALE."""
    vx, vy = _vettori_di(x), _vettori_di(y)
    if vx is not None or vy is not None:
        if vx is None or vy is None or vx[0] != vy[0]:
            return False, -1, "tipi strutturati diversi", None
        if vx[0] == "rng":
            ug = _stato_rng_uguale(vx[1], vy[1])
            return ug, (0 if ug else 1), ("" if ug else "stato del generatore diverso"), None
        fa, fb = vx[1], vy[1]
        if fa[0] != fb[0]:
            return False, -1, "forme diverse: %s contro %s" % (fa[0], fb[0]), None
        tot, mx = 0, 0.0
        for ca, cb in zip(fa[1:], fb[1:]):
            ug, nd, _nota, m = confronta(ca, cb)
            if not ug:
                tot += (nd if nd >= 0 else 1)
                if m is not None:
                    mx = max(mx, m)
        return tot == 0, tot, ("" if tot == 0 else "la matrice sparsa differisce"), mx
    if isinstance(x, np.ndarray) or isinstance(y, np.ndarray):
        a, b = np.asarray(x), np.asarray(y)
        if a.shape != b.shape:
            return False, -1, "forme diverse: %s contro %s" % (a.shape, b.shape), None
        if a.dtype.kind in "fc" and b.dtype.kind in "fc":
            af, bf = np.asarray(a, complex), np.asarray(b, complex)
            ug = (af == bf) | (np.isnan(af) & np.isnan(bf))
            nd = int(np.sum(~ug))
            mx = (float(np.nanmax(np.abs(af - bf))) if nd else 0.0)
            return nd == 0, nd, "", mx
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
        return tot == 0, tot, ("" if tot == 0 else "il dizionario differisce"), mx
    try:
        return (x == y), (0 if x == y else 1), "", None
    except Exception as e:
        return False, -1, "non confrontabile: %r" % (e,), None


def classe(nome):
    """`phi` / contatore / altro-stato. ### Un CONTATORE non e' uno STATO."""
    if nome == "phi":
        return "phi"
    if nome.startswith("_g_") or nome.startswith("_ritmo_") or nome.startswith("_tum_") \
            or nome.startswith("_cs_lam") or nome.startswith("_smp_") \
            or nome in ("_veleno_registro",):
        return "contatore/registro"
    return "STATO"


# =============================================================== LA SCENA
def carica(nome, sim, mem_fase=None):
    """La scena del DRIVER, `nmasse` e `sep` dall'ARGV (mai a mano).

    `mem_fase`: `None` = non si tocca *(il blob vecchio non ha il flag)*; `True`/`False` =
    si imposta ### **SUL MODULO**, che e' il modo prescritto dal `README` par. 9-bis.
    """
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        if mem_fase is not None:
            if not hasattr(S, "MEM_FASE"):
                raise SystemExit("[FERMO] `%s` non ha `MEM_FASE`: blob sbagliato." % nome)
            S.MEM_FASE = bool(mem_fase)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net, a


# =============================================================== BRACCIO 0
def braccio0():
    """### IL *PRIMA* VIENE DAL PADRE DEL COMMIT CHE HA CAMBIATO IL SIMULATORE.

    ### ⛔ **NON `HEAD~1`, e l'ha trovato il sigillo di `VELENO-ARCHI-KEEP` rifiutandosi
    di proseguire** *(`c7f2eb3`)*: dopo il commit della cura ne arriva un altro, e `HEAD~1`
    diventa **il commit della cura** -- il *prima* estratto sarebbe ### **GIA' CURATO.**
    ### **E il *prima* si verifica contro quello che LA PATCH DICHIARA**, non contro un
    numero scritto qui: due numeri in due posti sarebbero due leggi (`9-ter`).
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
    dst = os.path.join(FUORI, "_prima.py")
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
    patchato = os.path.join(FUORI, "_patchato.py")
    pr = subprocess.run([sys.executable, PATCH, dst, patchato],
                        capture_output=True, cwd=RADICE)
    out["patch_returncode"] = pr.returncode
    out["blob_patchato"] = blob(patchato)[:8] if os.path.isfile(patchato) else None
    out["blob_oggi"] = blob(SIM)[:8]
    out["coincide"] = bool(out["blob_patchato"] == out["blob_oggi"])
    out["stato"] = "fatto"
    return dst, out


# =============================================================== IL LOCKSTEP
def lockstep(passi, vecchio):
    """TRE bracci, confrontati su `vars(net)` INTERO a ogni passo."""
    SA, nA, a = carica("sim_mf_A", vecchio, None)          # il blob VECCHIO
    SB, nB, _ = carica("sim_mf_B", SIM, True)              # il nuovo, flag ACCESO
    SC, nC, _ = carica("sim_mf_C", SIM, False)             # il nuovo, DEFAULT (spento)
    in_conf = _cli_flag.dichiara_configurazione(SB, stampa)
    stampa("  flag sul modulo: A (vecchio) non ha MEM_FASE;  B = %s;  C = %s"
           % (getattr(SB, "MEM_FASE", "<assente>"), getattr(SC, "MEM_FASE", "<assente>")))
    stampa("  scena: nmasse=%s sep=%s  ->  n = %d, archi = %d"
           % (getattr(a, "nmasse", "?"), getattr(a, "sep", "?"), nA.n, len(nA.i)))
    stampa()
    riga("=")
    stampa("IL LOCKSTEP: %d passi, TRE bracci, col BATTITO per passo" % passi)
    riga("=")
    ab, bc = [], []
    for k in range(1, passi + 1):
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(SA, nA)
            _passo.passo_pieno(SB, nB)
            _passo.passo_pieno(SC, nC)
        d_ab = confronta_reti(nA, nB)
        d_bc = confronta_reti(nB, nC)
        ab.append({"passo": k, "diff": d_ab, "attributi": len(vars(nB))})
        bc.append({"passo": k, "diff": d_bc, "attributi": len(vars(nB))})
        print("[battito] passo %d/%d  n=%d archi=%d  A-B diff=%d  B-C diff=%d"
              % (k, passi, nB.n, len(nB.i), len(d_ab), len(d_bc)), flush=True)
    return ab, bc, in_conf, nA, nB, nC


def confronta_reti(n1, n2):
    """`vars(net)` INTERO: non un elenco scelto da me."""
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


# =============================================================== IL RAPPORTO
def rapporto(b0, ab, bc, in_conf, nA, nB, nC, passi):
    riga("=")
    stampa("BRACCIO 0: il *prima* NON si asserisce, SI RICOSTRUISCE")
    riga("=")
    for k in ["commit_che_ha_cambiato_il_simulatore", "padre", "blob_prima",
              "blob_prima_atteso", "prima_e_quello_atteso", "blob_patch",
              "blob_patchato", "blob_oggi", "patch_returncode", "coincide"]:
        if k in b0:
            stampa("  %-38s %s" % (k, b0[k]))
    stampa()

    riga("=")
    stampa("CRITERIO 1: A (blob VECCHIO) contro B (nuovo, MEM_FASE = True) -- AL BYTE")
    riga("=")
    tot_ab = [d for r in ab for d in r["diff"]]
    stato_ab = [d for d in tot_ab if d["classe"] == "STATO"]
    stampa("  passi confrontati: %d   attributi per passo: %d" % (len(ab), ab[0]["attributi"]))
    stampa("  differenze IN TOTALE: %d   di cui di STATO: %d" % (len(tot_ab), len(stato_ab)))
    if tot_ab:
        per = {}
        for d in tot_ab:
            per[d["nome"]] = per.get(d["nome"], 0) + 1
        for nome in sorted(per):
            stampa("      %-26s %-20s %d passi" % (nome, classe(nome), per[nome]))
    stampa()

    riga("=")
    stampa("CRITERI 2 e 3: B contro C (nuovo, DEFAULT = spento) -- AL PASSO 1")
    riga("=")
    p1 = bc[0]["diff"]
    stampa("  differenze al passo 1: %d" % len(p1))
    for d in p1:
        stampa("      %-26s %-20s quanti=%-10s max_scarto=%s  %s"
               % (d["nome"], d["classe"], d["quanti"],
                  ("%.6e" % d["max_scarto"]) if d["max_scarto"] is not None else "n/d",
                  d["nota"]))
    phi1 = [d for d in p1 if d["nome"] == "phi"]
    altri1 = [d for d in p1 if d["nome"] != "phi"]
    stampa("  `phi` differisce al passo 1: %s" % bool(phi1))
    stampa("  ALTRO che differisce al passo 1: %d" % len(altri1))
    stampa()

    riga("=")
    stampa("CRITERIO 4: la CRESCITA delle differenze per attributo, dal passo 2")
    riga("=")
    stampa("  ### SI RIPORTA, NON SI GIUDICA (il mandato lo dice).")
    stampa("  %-6s %-10s %s" % ("passo", "attributi", "i primi dieci nomi"))
    for r in bc:
        if r["passo"] in (1, 2, 3, 5, 10, 20, 40, 60, 80, 100, 120, 150) or \
                r["passo"] == len(bc):
            nomi = sorted({d["nome"] for d in r["diff"]})
            stampa("  %-6d %-10d %s%s" % (r["passo"], len(r["diff"]),
                                          ", ".join(nomi[:10]),
                                          " ..." if len(nomi) > 10 else ""))
    stampa()
    stampa("  E CHE COSA CAMBIA A VALLE, riportato e non giudicato:")
    stampa("      %-22s %-14s %-14s" % ("", "B (acceso)", "C (DEFAULT)"))
    for et, f in [("n finale", lambda x: x.n), ("archi finali", lambda x: len(x.i))]:
        stampa("      %-22s %-14s %-14s" % (et, f(nB), f(nC)))
    for et, k in [("divisioni (contatore)", "_g_div_tot"),
                  ("Schwinger (contatore)", "_g_sch_tot"),
                  ("nascite (contatore)", "_g_nascita_tot")]:
        vb, vc = getattr(nB, k, None), getattr(nC, k, None)
        if vb is not None or vc is not None:
            stampa("      %-22s %-14s %-14s" % (et, vb, vc))
    stampa()

    # ------------------------------------------------------------- l'esito
    guasti = []
    if not b0.get("coincide"):
        guasti.append("braccio 0: la patch NON ridA' il blob di oggi (%s)" % b0.get("stato"))
    if not ab:
        guasti.append("CRITERIO 1: zero passi confrontati -- zero NON e' un'identita'")
    if stato_ab:
        guasti.append("CRITERIO 1: %d differenze di STATO fra A e B: il flag ACCESO NON e' "
                      "byte-inerte" % len(stato_ab))
    if tot_ab and not stato_ab:
        guasti.append("CRITERIO 1: %d differenze NON di stato fra A e B, e vanno guardate"
                      % len(tot_ab))
    if not phi1:
        guasti.append("CRITERIO 3 (il caso che DEVE fallire): col flag spento `phi` NON "
                      "differisce al passo 1 -- lo spegnimento non spegne niente")
    if altri1:
        guasti.append("CRITERIO 2: al passo 1 differisce ANCHE: %s"
                      % ", ".join(sorted({d["nome"] for d in altri1})))
    if not in_conf:
        guasti.append("la configurazione NON e' quella del driver: il sigillo e' di un "
                      "ALTRO sistema")
    riga("=")
    stampa("L'ESITO")
    riga("=")
    if guasti:
        stampa("  ### IL SIGILLO NON PASSA, e mi FERMO. Che cosa non torna:")
        for g in guasti:
            stampa("      - " + g)
        stampa("  ### NON AMMORBIDISCO I CRITERI: erano fissati PRIMA, in 634762c.")
        riga("=")
        return 1, guasti
    stampa("  ### IL SIGILLO PASSA:")
    stampa("      braccio 0: la patch su %s ridA' %s AL BYTE"
           % (b0["blob_prima"], b0["blob_oggi"]))
    stampa("      criterio 1: ZERO differenze fra A e B su %d passi e %d attributi"
           % (len(ab), ab[0]["attributi"]))
    stampa("      criterio 2: al passo 1 differisce SOLO `phi`")
    stampa("      criterio 3: e `phi` DIFFERISCE -- lo spegnimento spegne")
    stampa("      criterio 4: la crescita e' riportata sopra, senza giudizio")
    riga("=")
    return 0, []


def main(argv):
    passi = PASSI
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    riga("=")
    stampa("IL SIGILLO DELLA CURA (2) DI MEM-HEBB-VERSO: il flag `MEM_FASE`")
    riga("=")
    stampa()
    pf = piattaforma()
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa("  simulatore OGGI %s" % blob(SIM)[:8])
    stampa("  patch          %s" % blob(PATCH)[:8])
    stampa()
    vecchio, b0 = braccio0()
    if vecchio is None:
        riga("=")
        stampa("BRACCIO 0: NON si e' potuto ricostruire il *prima*. MI FERMO.")
        for k, v in b0.items():
            stampa("  %-38s %s" % (k, v))
        riga("=")
        _scrivi({"braccio0": b0, "esito": 1, "piattaforma": pf})
        return 1
    ab, bc, in_conf, nA, nB, nC = lockstep(passi, vecchio)
    esito, guasti = rapporto(b0, ab, bc, in_conf, nA, nB, nC, passi)
    _scrivi({"braccio0": b0, "esito": esito, "guasti": guasti, "piattaforma": pf,
             "passi": passi, "blob_sim_oggi": blob(SIM), "blob_patch": blob(PATCH),
             "in_configurazione_del_driver": bool(in_conf),
             "attributi_per_passo": ab[0]["attributi"] if ab else 0,
             "A_contro_B": ab, "B_contro_C": bc,
             "a_valle": {"n_B": int(nB.n), "n_C": int(nC.n),
                         "archi_B": int(len(nB.i)), "archi_C": int(len(nC.i))},
             "timbro_strumento": _timbro()})
    return esito


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
