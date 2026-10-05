# -*- coding: utf-8 -*-
"""IL SIGILLO DELLA CURA DI `VELENO-ARCHI-KEEP`, via (i).

*(Decisione di Luca del 2026-10-05. Criteri fissati **PRIMA** in
`doc/TASK_HISTORY/2026-10-05_veleno-archi-keep-cura.md`, e quelli di `923e396` restano.)*

### I CRITERI CHE QUESTO STRUMENTO COPRE
| | |
|---|---|
| **`0`** | **braccio 0**: il *prima*, estratto dal **PADRE** del commit *(`H-P8`)*, + la patch committata = il blob di **oggi**, AL BYTE |
| ### **`1`** | ### **STATO IDENTICO AL BYTE su tutti i 150 passi**, lockstep su **TUTTI** gli attributi di `net` |
| **`2`** | le eccezioni ammesse sono **`_dt_e_ultimo`** e **`_sin2_vir`** |

### I CRITERI `3`-`7` NON STANNO QUI, ED E' UNA SCELTA MISURATA
Il criterio `3` *(negli eventi **Schwinger** anche le due derivate sono identiche)*
### **non e' testabile a granularita' di PASSO**, e non per una mia comodita': il passo (1)
ha misurato che ### **NESSUNO dei 64 eventi Schwinger sta in un passo senza divisione**
*(`64` su `64` hanno anche una divisione)*. ### **Quindi va letto a granularita' di EVENTO,
e lo strumento che aggancia `nascita` esiste gia': `425b8d47`.**
### ➜ **I criteri `3`, `4`, `5`, `6`, `7` si leggono rigirando i DUE strumenti committati**
*(`425b8d47` e `19d08753`)*, come il mandato prescrive. ### **Non li ri-implemento qui:
sarebbe un secondo strumento per lo stesso lavoro** *(`9-ter`)*.

### IL LOCKSTEP, e perche' confronta TUTTO
Due moduli caricati dal **CLI** *(mai a mano: `H-P3`)*, stessa `argv`, stesso seme, e dopo
**ogni** passo si confrontano **tutti** gli attributi di `net` -- ndarray e scalari.
### **Non un elenco scelto da me: `vars(net)` intero.** Un elenco sarebbe la lista delle
cose a cui ho pensato, e ### **il difetto che un sigillo deve prendere e' quello a cui non
ho pensato.**

### E LA CLASSIFICA DELLE DIFFERENZE E' IL PUNTO
| classe | che cos'e' |
|---|---|
| ### **STATO** | ### **qualunque differenza qui e' un FALLIMENTO** |
| **derivate ammesse** | `_dt_e_ultimo`, `_sin2_vir` *(criterio `2`)* |
| **contatori / registro del veleno** | `_g_*`, `_veleno_registro`: ### **conseguenze aritmetiche della cura, DICHIARATE nel task history PRIMA di misurare** |

USO:
  python csv/_seal_fork/_sigillo_veleno_keep.py
  opzioni: --passi=N (default 150)

USCITA: `csv/_seal_fork/_sigillo_veleno_keep/_sigillo.json` + `_corsa.txt`.

# ESENTE-H-P8: il *prima* NON viene da `HEAD`, viene dal PADRE -- `git rev-parse HEAD~1`,
#   e il blob si estrae con `git cat-file -p <padre>:soliton_simulator.py` IN BINARIO
#   (par.7: mai `git checkout`). Il hook cerca la sottostringa `HEAD`, e `HEAD~1` la
#   contiene: e' un falso positivo, e il hook ha ragione a guardare.
#   ### E NON LO AGGIRO RISCRIVENDO `@~1`, che passerebbe il controllo senza cambiare
#   niente: sarebbe DISARMARE UN PRESIDIO CAMBIANDO LE PAROLE, ed e' esattamente
#   l'errore che `H-FILE` ha fatto su se stesso il 2026-10-04 (il messaggio CITAVA la
#   via d'uscita, e il presidio si disattivava parlando di se'). Si dichiara, e si
#   lascia il controllo a guardare.
#   ### E IL BRACCIO 0 VERIFICA CHE IL *PRIMA* SIA GIUSTO: il blob estratto deve essere
#   `0f060670`, e la patch committata deve portarlo al blob di oggi AL BYTE. Se il
#   `prima` fosse sbagliato, il braccio 0 NON tornerebbe.
# ESENTE-H-P3: i due moduli si caricano TUTTI E DUE passando dal `_cli()` del simulatore
#   (`_cli_flag.carica_dal_cli`), con la stessa argv del driver. Nessun attributo di modulo
#   e' assegnato a mano. Il `prima` si estrae dal PADRE del commit, in binario (par.7).
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
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_veleno_keep")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PATCH = os.path.join(RADICE, "csv", "_seal_fork", "_veleno_keep_patch.py")
PASSI = 150
# ### LE DUE DERIVATE AMMESSE: non un elenco mio, il criterio 2 del mandato.
AMMESSE = ("_dt_e_ultimo", "_sin2_vir")

P = []


def stampa(s=""):
    print(s)
    P.append(s)


def riga(c="-"):
    stampa(c * 104)


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def git(*a):
    return subprocess.run(["git", "-C", RADICE] + list(a), capture_output=True)


def classe(nome):
    """### STATO, derivata ammessa, o contabilita' del veleno?"""
    if nome in AMMESSE:
        return "derivata ammessa"
    if nome.startswith("_g_") or nome == "_veleno_registro":
        return "contatore/registro"
    return "STATO"


def confronta(x, y):
    """-> (uguale, quanti_diversi, nota). `NaN` contro `NaN` e' UGUALE."""
    if isinstance(x, np.ndarray) or isinstance(y, np.ndarray):
        if not (isinstance(x, np.ndarray) and isinstance(y, np.ndarray)):
            return False, -1, "uno e' ndarray e l'altro no"
        if x.shape != y.shape:
            return False, -1, "forme diverse: %s contro %s" % (x.shape, y.shape)
        if x.dtype != y.dtype:
            return False, -1, "dtype diversi: %s contro %s" % (x.dtype, y.dtype)
        if x.dtype.kind in "fc":
            ug = (x == y) | (np.isnan(x) & np.isnan(y))
        else:
            ug = (x == y)
        d = int(np.sum(~ug))
        return d == 0, d, ""
    if isinstance(x, float) and isinstance(y, float):
        if np.isnan(x) and np.isnan(y):
            return True, 0, ""
    if type(x) is not type(y):
        return False, -1, "tipi diversi: %s contro %s" % (type(x).__name__,
                                                          type(y).__name__)
    try:
        return (x == y), (0 if x == y else 1), ""
    except Exception as e:
        return False, -1, "non confrontabile: %r" % (e,)


def carica(nome, sim):
    """La scena del DRIVER, `nmasse` e `sep` dall'ARGV (mai a mano)."""
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net, a


def braccio0():
    """### IL *PRIMA* VIENE DAL PADRE DEL COMMIT, non da `HEAD` (`H-P8`), e si estrae
    in BINARIO (par.7: `git cat-file -p`, non `git checkout`)."""
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    out = {"dove": "il PADRE del commit (H-P8)"}
    r = git("rev-parse", "HEAD~1")
    padre = r.stdout.decode().strip()
    out["padre"] = padre
    q = git("cat-file", "-p", padre + ":soliton_simulator.py")
    if q.returncode != 0:
        out["stato"] = "non estratto dal padre"
        return None, out
    dst = os.path.join(FUORI, "_sim_prima.py")
    io.open(dst, "wb").write(q.stdout)
    out["blob_prima"] = blob(dst)[:8]
    # la patch committata, applicata alla copia
    cop = os.path.join(FUORI, "_sim_prima_patchato.py")
    io.open(cop, "wb").write(q.stdout)
    pr = subprocess.run([sys.executable, PATCH, "--file=" + cop],
                        capture_output=True, cwd=RADICE)
    out["patch_returncode"] = pr.returncode
    out["blob_patchato"] = blob(cop)[:8]
    out["blob_oggi"] = blob(SIM)[:8]
    out["blob_patch"] = blob(PATCH)[:8]
    out["coincide"] = bool(out["blob_patchato"] == out["blob_oggi"])
    out["stato"] = "fatto"
    return dst, out


def principale(passi):
    riga("=")
    stampa("IL SIGILLO DELLA CURA DI `VELENO-ARCHI-KEEP`, via (i)")
    riga("=")
    stampa()
    pf = {"python": sys.version.split()[0], "numpy": np.__version__,
          "sistema": platform.system() + " " + platform.release(),
          "macchina": platform.machine()}
    for k in ["python", "numpy", "sistema", "macchina"]:
        stampa("  %-10s %s" % (k, pf[k]))
    stampa()

    riga("=")
    stampa("BRACCIO 0 -- il *prima* dal PADRE del commit, + la patch committata")
    riga("=")
    prima_file, b0 = braccio0()
    for k in ["padre", "blob_prima", "blob_patch", "blob_patchato", "blob_oggi",
              "patch_returncode", "coincide"]:
        if k in b0:
            stampa("  %-18s %s" % (k, b0[k]))
    if prima_file is None or not b0.get("coincide"):
        stampa("  ### FERMO: il braccio 0 NON torna. Senza di lui il confronto che segue")
        stampa("      non parte da un punto verificabile.")
        riga("=")
        return 1, {"braccio0": b0}
    stampa("  ### IL BRACCIO 0 TORNA: il punto di partenza non e' asserito, e' verificato.")
    stampa()

    riga("=")
    stampa("IL LOCKSTEP: %d passi, TUTTI gli attributi di `net` dopo OGNI passo" % passi)
    riga("=")
    SA, netA, aA = carica("sim_prima_sig", prima_file)
    SB, netB, aB = carica("sim_dopo_sig", SIM)
    stampa("  scena: nmasse=%s sep=%s" % (getattr(aA, "nmasse", "?"),
                                          getattr(aA, "sep", "?")))
    stampa("  PRIMA: n=%d archi=%d    DOPO: n=%d archi=%d"
           % (netA.n, len(netA.i), netB.n, len(netB.i)))
    if netA.n != netB.n or len(netA.i) != len(netB.i):
        stampa("  ### FERMO: le due scene non partono uguali.")
        return 1, {"braccio0": b0, "scena": "diversa"}

    per_passo = []
    stato_div = []
    for k in range(1, passi + 1):
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(SA, netA)
            _passo.passo_pieno(SB, netB)
        va, vb = vars(netA), vars(netB)
        nomi = sorted(set(va) | set(vb))
        riassunto = {"passo": k, "attributi": len(nomi), "diff": []}
        for nome in nomi:
            if nome not in va or nome not in vb:
                riassunto["diff"].append({"nome": nome, "classe": classe(nome),
                                          "nota": "presente in uno solo",
                                          "solo_in": "PRIMA" if nome in va else "DOPO"})
                continue
            ug, nd, nota = confronta(va[nome], vb[nome])
            if not ug:
                riassunto["diff"].append({"nome": nome, "classe": classe(nome),
                                          "diversi": nd, "nota": nota})
        for d in riassunto["diff"]:
            if d["classe"] == "STATO":
                stato_div.append(dict(d, passo=k))
        per_passo.append(riassunto)
        print("[battito] passo %d/%d  nA=%d nB=%d  diff=%d  di cui STATO=%d"
              % (k, passi, netA.n, netB.n, len(riassunto["diff"]),
                 sum(1 for d in riassunto["diff"] if d["classe"] == "STATO")),
              flush=True)

    stampa("  passi girati: %d" % passi)
    stampa("  attributi confrontati per passo: %d" % per_passo[-1]["attributi"])
    stampa()

    # ------------------------------------------------- la classifica
    riga("=")
    stampa("LE DIFFERENZE, PER CLASSE")
    riga("=")
    per_classe = {}
    per_nome = {}
    for r in per_passo:
        for d in r["diff"]:
            per_classe[d["classe"]] = per_classe.get(d["classe"], 0) + 1
            per_nome.setdefault(d["nome"], {"classe": d["classe"], "passi": 0})
            per_nome[d["nome"]]["passi"] += 1
    for cl in ("STATO", "derivata ammessa", "contatore/registro"):
        stampa("  %-22s %6d confronti diversi" % (cl, per_classe.get(cl, 0)))
    stampa()
    stampa("  %-26s %-20s %8s" % ("attributo", "classe", "passi"))
    riga()
    for nome in sorted(per_nome, key=lambda x: (per_nome[x]["classe"], x)):
        v = per_nome[nome]
        stampa("  %-26s %-20s %8d" % (nome[:26], v["classe"], v["passi"]))
    riga()
    stampa()

    # ------------------------------------------------- i criteri
    riga("=")
    stampa("I CRITERI 0, 1, 2")
    riga("=")
    esito = 0
    stampa("  (0) braccio 0: %s" % ("TORNA" if b0.get("coincide") else "### NON TORNA"))
    stampa("  (1) STATO identico al byte: differenze di STATO = %d" % len(stato_div))
    if stato_div:
        stampa("  ### FERMO: lo STATO DIVERGE. E non e' un difetto di questa cura: vuol")
        stampa("      dire che la conclusione di cb24b95 -- <<nessun lettore vivo legge")
        stampa("      queste derivate dopo la nascita>> -- ERA SBAGLIATA.")
        for d in stato_div[:10]:
            stampa("      passo %-4s %-24s %s"
                   % (d["passo"], d["nome"], d.get("nota") or
                      ("%d elementi diversi" % d.get("diversi", -1))))
        esito = 1
    else:
        stampa("      ### ZERO differenze di STATO su %d passi." % passi)
    amm = sorted(n for n, v in per_nome.items() if v["classe"] == "derivata ammessa")
    extra = sorted(n for n, v in per_nome.items() if v["classe"] == "contatore/registro")
    stampa("  (2) derivate che differiscono: %s" % (amm or "nessuna"))
    stampa("      e le eccezioni AMMESSE dal criterio 2 sono: %s" % list(AMMESSE))
    fuori_crit = [n for n in amm if n not in AMMESSE]
    if fuori_crit:
        stampa("  ### FERMO: differiscono derivate FUORI dalle due ammesse: %s" % fuori_crit)
        esito = 1
    stampa()
    stampa("  ### E GLI ATTRIBUTI DI CONTABILITA' CHE DIFFERISCONO, dichiarati nel task")
    stampa("      history PRIMA di misurare e NON compresi fra le eccezioni del mandato:")
    for n in extra:
        stampa("      %-26s (%d passi)" % (n, per_nome[n]["passi"]))
    stampa("      ### Nessuno di questi e' STATO. ### L'elenco delle eccezioni del")
    stampa("          criterio 2 li comprenda o no e' UNA DECISIONE DI LUCA, e questo")
    stampa("          referto gliela mette davanti coi numeri.")
    riga("=")

    fuori = {"piattaforma": pf, "braccio0": b0, "passi": passi,
             "timbro_strumento": _presidio.timbro(__file__),
             "blob_sim_oggi": blob(SIM), "blob_patch": blob(PATCH),
             "attributi_per_passo": per_passo[-1]["attributi"],
             "per_classe": per_classe, "per_nome": per_nome,
             "stato_divergenze": stato_div[:200],
             "n_stato_divergenze": len(stato_div),
             "derivate_diverse": amm, "contabilita_diversa": extra,
             "ammesse": list(AMMESSE), "esito": esito}
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    json.dump(fuori, io.open(os.path.join(FUORI, "_sigillo.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False, sort_keys=True, default=str)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(NL.join(P))
    print("scritto: %s" % os.path.join(FUORI, "_sigillo.json"))
    return esito, fuori


if __name__ == "__main__":
    pp = PASSI
    for _a in sys.argv[1:]:
        if _a.startswith("--passi="):
            pp = int(_a.split("=", 1)[1])
    _e, _f = principale(pp)
    sys.exit(_e)
