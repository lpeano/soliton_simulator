# -*- coding: utf-8 -*-
"""`CURA 4` -- **IL SIGILLO DELL'ACCENSIONE DEL CAMPO** (`SEMINA_MATURA`).

**I criteri sono stati fissati PRIMA, nel task history**
`doc/TASK_HISTORY/2026-09-25_cura-accensione-campo.md`, **committato prima del codice**
*(par.5-septies: l'ordine e' verificabile da git)*.

```
A1  flag SPENTO = BYTE-IDENTICO, firma dei byte su tutti i campi     un processo per braccio
A2  al passo 1, `ramp == 1` su TUTTI i nodi della semina iniziale    ESATTO, non approssimato
A3  un nodo nato da MITOSI parte da `ramp = 0` e arriva a 1 nel suo TEMPO-LUCE
A4  contrasto massa/vuoto e `Lam` al passo 1, contro `P2 = 27` e `P3 = 5`
A5  CONTROLLO POSITIVO: ON e OFF **DEVONO** differire al passo 1
A6  CASO CHE DEVE FALLIRE: con `maturi=False` forzato, `A2` deve dare FAIL
A7  `TAU_A` non e' piu' letto da `_pesi` -- verifica dall'AST, non da un `grep`
```

**`STANDARD 1`** *(un processo per braccio)* e **`STANDARD 2`** *(firma dei byte, non `max|delta|`:
`array_equal` dice `False` per due array di `NaN` byte-identici)*. ASCII puro nel sorgente.
"""
import hashlib
import ast
import io
import json
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _cli_flag
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
FUORI = os.path.join(_QUI, "_sig_cura4")
DEST = os.path.join(FUORI, "SIGILLO_cura4_accensione.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEME = 11
SEP = 4.0          # la scena (ii) (b): la piu' economica

# ========================================================================================
# [`CLI-1`, mandato di Luca 2026-09-25] **I BRACCI SI CONFIGURANO DAL CLI, NON DAL MODULO.**
# ----------------------------------------------------------------------------------------
# La prima stesura di questo sigillo faceva `S.SEMINA_MATURA = bool(FLAG)` **sul modulo**.
# **E' per questo che dava `7/7` mentre il flag era MORTO da riga di comando** (assegnazione
# in `esegui_headless`, `global` in `_applica_flag`: una **locale silenziosamente inerte**).
#   ### UN SIGILLO CHE IMPOSTA IL MODULO A MANO PROVA LA LEGGE, NON IL FLAG.
# Ora l'argv **si CATTURA dal driver** (`csv/_cli_flag.py`, la stessa funzione che usa il
# sigillo del driver: **una sola implementazione**) e ogni braccio passa da `_cli()` +
# `_applica_flag(a)`.
# **IL BRACCIO OFF E' L'ARGV MENO L'OPZIONE**, perche' i flag sono `store_true` e
# **`--semina-matura=off` NON ESISTE**: l'unico OFF che il CLI ammette e' *un comando che
# DIMENTICA il flag* -- che e' anche il difetto contro cui il sigillo del driver monta la
# guardia. E il driver **non puo'** darlo: accende le obbligatorie senza `if`, di proposito.
OPZ = "--semina-matura"
FLAGNOME = "SEMINA_MATURA"
SIM_HEAD = os.path.join(RADICE, "soliton_simulator.py")
ARGV = _cli_flag.argv_del_driver([], dest=os.path.join(TMP, "_scarto"))[1]
# ⚠ **`--nodi 0` SI AGGIUNGE, E VA DICHIARATO PERCHE' NON E' L'ARGV DEL DRIVER.**
#   `_applica_flag` **semina il vuoto di default** (`SCENA-1`), ma **il figlio lo BUTTA**:
#   fa `S.net = S.Rete(SEME)` e costruisce la scena `(ii)`. Quel vuoto non e' ne' misurato
#   ne' confrontato -- e' solo costo.
#   **E sul braccio «prima» era un ARRESTO:** il codice precedente non ha la `SCENA-1`,
#   quindi semina `a.nodi = 900` **con `--semina-lam` acceso**, e
#   `[semina-lam] RIFIUTO DI SEMINARE: non ci stanno 900 nodi a distanza >= LAM` **ferma il
#   braccio**. E' **esattamente il conflitto che `S5` misura**, visto dal codice di prima:
#   **la conferma indipendente che `SCENA-1` era necessaria**, non un intoppo del sigillo.
ARGV = ARGV + ["--nodi", "0"]
assert OPZ in ARGV, ("il driver NON passa %s: il braccio OFF sarebbe IDENTICO " % OPZ)

FIGLIO = r'''
import hashlib, io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import _cli_flag
# [`CLI-1`] IL FLAG ARRIVA DAL CLI. **Nessun attributo assegnato a mano**: si passa
#   l'argv VERA DEL DRIVER a `_cli()` + `_applica_flag(a)`, e il braccio OFF e' la stessa
#   argv MENO l'opzione. `argv_per` toglie in piu' le opzioni che QUEL simulatore non
#   dichiara (serve al braccio «prima», che non conosce le opzioni nate dopo di lui).
_argv, _scartate = _cli_flag.argv_per(SIM, ARGV if FLAG else _cli_flag.senza(ARGV, OPZ))
S, _a_cli = _cli_flag.carica_dal_cli(_argv, nome="sim_c4", sim=SIM)
# ⚠ E SI VERIFICA CHE IL CLI ABBIA DAVVERO ACCESO: senza questo, un flag morto
#   ripasserebbe in silenzio, che e' esattamente cio' che e' successo.
_CLI = {"flag": getattr(S, FLAGNOME, "ASSENTE"), "atteso": bool(FLAG),
        "semina_lam": getattr(S, "SEMINA_LAM", "ASSENTE"),
        "opz_nell_argv": OPZ in _argv, "argv_len": len(_argv),
        "scartate": _scartate, "sim": os.path.basename(SIM)}
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
if MATURI_FORZATO is not None:
    # `A6`, IL CASO CHE DEVE FALLIRE: si forza `maturi=False` avvolgendo `semina`.
    _orig = S.Rete.semina
    def _sem(self, n, raggio=None, centro=(0, 0, 0), fase=None, mass_id=None, maturi=None):
        return _orig(self, n, raggio=raggio, centro=centro, fase=fase, mass_id=mass_id,
                     maturi=bool(MATURI_FORZATO))
    S.Rete.semina = _sem
S._semina_masse_coerenti()
net = S.net
co = S.test["dati"]["coorti"]
n0 = int(net.n)
iniz = np.arange(n0)                      # TUTTI i nodi della semina iniziale

o = dict(FLAG=bool(FLAG), MATURI_FORZATO=MATURI_FORZATO, CLI=_CLI, n0=n0, archi0=int(len(net.d)),
         TAU_A=float(S.TAU_A), DT=float(S.DT))

def _ramp(net):
    # ⚠ SUL CODICE DI PRIMA `_tempo_rampa` NON ESISTE: l'ha introdotta la cura 4. La
    #   rampa del vecchio e' `eta/TAU_A`, **LETTA DAL SORGENTE VECCHIO** (`:3537` di
    #   `900fe603^`: `ramp = np.minimum(1.0, self.eta / TAU_A)`), **non indovinata**.
    #   ✅ **E CHE QUESTO RAMO SERVA E' LA PROVA CHE `A1` ERA VACUO:** finche' il codice
    #   «di prima» era `HEAD`, `_tempo_rampa` **c'era** -- perche' HEAD conteneva la cura.
    #   **Un braccio che non poteva nemmeno GIRARE sul codice vero stava passando da giorni.**
    _tr = net._tempo_rampa() if hasattr(net, "_tempo_rampa") else S.TAU_A
    return np.minimum(1.0, np.asarray(net.eta, float) / _tr)

o["ramp0_min"] = float(_ramp(net).min()); o["ramp0_max"] = float(_ramp(net).max())
o["eta0_p50"] = float(np.median(net.eta))
o["pesi0_somma"] = float(np.sum(net._pesi()))

net.step()                                 # IL PASSO 1
r1 = _ramp(net)
o["n1"] = int(net.n)
o["ramp1_iniz_min"] = float(r1[iniz].min()); o["ramp1_iniz_max"] = float(r1[iniz].max())
o["ramp1_iniz_uguali_1"] = int(np.sum(r1[iniz] == 1.0))
o["pesi1_somma"] = float(np.sum(net._pesi()))
net.calcola_psi()
I = np.asarray(net.intensita(), float)
co1 = {k: v[v < net.n] for k, v in co.items()}
dentro = np.concatenate([co1["massa_%d" % k] for k in range(3)])
o["I_massa"] = float(I[dentro].mean()); o["I_vuoto"] = float(I[co1["vuoto"]].mean())
o["contrasto"] = (o["I_massa"] / o["I_vuoto"]) if o["I_vuoto"] else float("inf")
o["Lam"] = float(I.mean())
# ⚠ `_g_rampa_prec` NON E' UN CONTATORE: e' la MEMORIA PER NODO della rampa del passo
#   prima, un `ndarray(n,)`. Nel json ne va la FORMA, non i valori -- e va detto invece di
#   toglierla in silenzio: chi legge il json deve sapere che quel campo non e' un numero.
#   *(Il primo giro dal CLI e' morto qui: `TypeError: ndarray is not JSON serializable`,
#   e NON era morto prima perche' a flag spento quel ramo non scriveva l'array.)*
o["g_rampa"] = {}
for _k, _v in vars(net).items():
    if not (_k.startswith("_g_rampa") or _k.startswith("_g_cura4")):
        continue
    if isinstance(_v, np.ndarray):
        o["g_rampa"][_k] = ["ndarray", list(_v.shape)]
    else:
        o["g_rampa"][_k] = list(_v) if isinstance(_v, tuple) else _v

# FIRMA DEI BYTE su tutti i campi confrontabili (`STANDARD 2`)
firme = {}
for k, v in sorted(vars(net).items()):
    if k.startswith("_g_") or k.startswith("_cura4"):
        continue
    if isinstance(v, np.ndarray):
        firme[k] = [hashlib.sha1(np.ascontiguousarray(v).tobytes()).hexdigest()[:12],
                    list(v.shape), str(v.dtype)]
    elif isinstance(v, (int, float, bool, str)):
        firme[k] = [hashlib.sha1(repr(v).encode()).hexdigest()[:12], [], type(v).__name__]
o["firme"] = firme
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  n %d -> %d  pesi0 %.6e  pesi1 %.6e" % (NOME, n0, net.n, o["pesi0_somma"],
                                                     o["pesi1_somma"]))
'''

# ------------------------------------------------- `A3`: la MITOSI, forzata nella finestra
FIGLIO_MIT = r'''
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
import importlib.util as _iu
sys.path.insert(0, os.path.join(RAD, "csv"))
import _cli_flag
_argv, _scartate = _cli_flag.argv_per(SIM, ARGV)     # [`CLI-1`] il flag dal CLI
S, _a_cli = _cli_flag.carica_dal_cli(_argv, nome="sim_c4m", sim=SIM)
_CLI = {"flag": getattr(S, FLAGNOME, "ASSENTE"), "atteso": True,
        "semina_lam": getattr(S, "SEMINA_LAM", "ASSENTE"),
        "opz_nell_argv": OPZ in _argv, "argv_len": len(_argv),
        "scartate": _scartate, "sim": os.path.basename(SIM)}
net = S.Rete(7)
net.semina(60)                # rete piccola: `A3` misura UN nodo, non una statistica
net.step()                    # senza, `_rho_sorgente()` e' vuoto e `mitosi` si SCHIANTA (FRAG1)
n_pre = int(net.n)
# LA FINESTRA DI CREAZIONE SI DERIVA DAL CODICE (par.9), non si sceglie:
_s0 = (S.PHI_CRIT + np.pi) if (S.TORS_4PI and not S.FASE_2PI) else S.PHI_CRIT
_centro = 0.5 * ((1.0 + _s0 / S.PHI_CRIT) + (1.0 + (4.0 * np.pi) / S.PHI_CRIT))
TW0 = 0.5 * (_s0 + (_centro - 1.0) * S.PHI_CRIT)
# ⚠⚠ [`CLI-1`, 2026-09-25] **L'ARCO SI SCEGLIE CONFORME A `A13`, NON SI PRENDE IL PRIMO.**
#   Dal CLI arriva **anche `--mitosi-2lam`** (e'e' obbligatoria), quindi la
#   `CURA 5` e' ATTIVA: **un arco si divide solo se `d >= 2 LAM`.** L'arco `0` di questo
#   telaio misura `d = 1.1433` contro `2 LAM = 1.6000`, quindi **la cura 5 ne VIETAVA la
#   divisione** e `A3` non aveva piu' niente da misurare: `nuovi 0`.
#   **NON si spegne la cura 5 e NON si fabbrica una lunghezza:** si prende **l'arco piu'
#   LUNGO**, che nel telaio conforma gia' (`d = 2.3939 >= 1.6000`, e 154 archi su 224 lo
#   fanno). **«Arco 0» era una scelta arbitraria; «il piu' lungo» e' un criterio.**
#   ✅ **E questo e' un riscontro del passaggio dal CLI**: il sigillo di una cura girava
#   in una configurazione in cui **l'altra cura approvata non c'era**.
_karc = int(np.argmax(np.asarray(net.d, float)))
net.tw = np.zeros(len(net.d)); net.tw[_karc] = TW0
o_arco = {"arco": _karc, "d_arco": float(np.asarray(net.d, float)[_karc]),
          "due_lam": float(2.0 * S.LAM),
          "conformi": int(np.sum(np.asarray(net.d, float) >= 2.0 * S.LAM)),
          "archi": int(len(net.d))}
_rng = net.rng
class _R:
    def __getattr__(self, k): return getattr(_rng, k)
    def random(self, *a, **k):
        _n = a[0] if a else k.get("size")
        return np.zeros(_n) if _n is not None else 0.0
net.rng = _R()
net.mitosi()
nuovi = np.arange(n_pre, net.n)
o = dict(n_pre=n_pre, n_post=int(net.n), nuovi=int(nuovi.size), TW0=float(TW0),
         arco=o_arco)
def _ramp(net):
    _tr = net._tempo_rampa()
    return np.minimum(1.0, np.asarray(net.eta, float) / _tr), _tr
if nuovi.size:
    r, tr = _ramp(net)
    o["eta_nuovi"] = [float(x) for x in net.eta[nuovi]]
    o["ramp_nuovi_alla_nascita"] = [float(x) for x in r[nuovi]]
    o["tempo_luce_nuovi"] = [float(np.asarray(tr, float)[k]) for k in nuovi] if np.ndim(tr) else float(tr)
    # quanti passi servono perche' ARRIVI a 1? si conta girando.
    passi = 0
    while passi < 400:
        net.step(); passi += 1
        r, tr = _ramp(net)
        if nuovi.max() < net.n and float(r[nuovi].min()) >= 1.0:
            break
    o["passi_per_ramp1"] = passi
    o["ramp_finale"] = float(r[nuovi[nuovi < net.n]].min()) if nuovi.max() < net.n else float("nan")
    o["tempo_luce_finale"] = (float(np.median(np.asarray(tr, float))) if np.ndim(tr) else float(tr))
o["CLI"] = _CLI
io.open(os.path.join(TMPD, "mitosi.json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK mitosi  n %d -> %d  nuovi %d" % (n_pre, net.n, nuovi.size))
'''


def braccio(nome, flag, maturi=None, sorgente=FIGLIO, sim=None, argv=None):
    """UN PROCESSO per braccio (`STANDARD 1`), configurato DAL CLI.

    `sim` permette di far girare lo STESSO figlio sul simulatore PRECEDENTE alla cura
    (braccio `A1`): prima c'erano DUE funzioni e una `str.replace` sul sorgente del
    figlio per togliere l'assegnazione del flag. **Passando dal CLI quella replace non
    serve piu': non c'e' nessuna assegnazione da togliere** (`STANDARD 10`: una cura
    non aumenta il numero delle leggi, e qui ne toglie una).
    """
    testa = ["RAD = %r" % RADICE, "TMPD = %r" % TMP, "NOME = %r" % nome,
             "SEME = %d" % SEME, "SEP = %r" % SEP, "FLAG = %r" % flag,
             "MATURI_FORZATO = %r" % maturi, "SIM = %r" % (sim or SIM_HEAD),
             "ARGV = %r" % (ARGV if argv is None else argv),
             "OPZ = %r" % OPZ, "FLAGNOME = %r" % FLAGNOME, ""]
    src = chr(10).join(testa) + sorgente
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline=chr(10)).write(src)
    return subprocess.run([sys.executable, p], cwd=RADICE, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def leggi(nome):
    return json.loads(io.open(os.path.join(TMP, nome + ".json"), encoding="utf-8").read())


LOG = []
BR = [("off", False, None), ("on", True, None), ("on_forzato", True, False)]
for nome, flag, mat in BR:
    rr = braccio(nome, flag, mat)
    LOG.append("[%s] rc=%d %s" % (nome, rr.returncode, (rr.stdout or "").strip()[-150:]))
    if rr.returncode:
        LOG.append((rr.stderr or "")[-1400:])
# ==========================================================================================
# `A1`: IL RAMO SPENTO CONTRO IL CODICE PRECEDENTE -- **E IL CRITERIO ERA SCADUTO**
# ------------------------------------------------------------------------------------------
# ❌ **DIFETTO MIO, trovato il 2026-09-25 rifacendo il sigillo per `CLI-1`:** il codice
#   «di prima» si prendeva da **`HEAD:soliton_simulator.py`**. Era giusto **finche' la cura
#   non era committata**; **dal commit della cura in poi HEAD LA CONTIENE**, e il braccio
#   «prima» e' diventato **il braccio OFF di se stesso** -- un confronto che passa per
#   costruzione. **NON era vacuo quando l'ho scritto: LO E' DIVENTATO**, ed e' la famiglia
#   di `T1` (par.0: *un criterio SCADUTO che confronta il disco di OGGI con un blob di ieri*).
# ✅ **CURA, la stessa di `T1`: si ancora alla COPPIA DI BLOB CHE RACCHIUDE IL CAMBIAMENTO.**
#   `sim_prima_del_flag` trova il commit che ha INTRODOTTO il flag (`git log -S`, la voce
#   piu' vecchia), ne prende il PADRE, estrae in BINARIO (trappola CRLF, par.5-quinquies) e
#   **ASSERISCE che il file estratto NON contenga il flag**: se l'ancora fosse sbagliata
#   **si ferma invece di misurare niente** (`A9`).
VECCHIO = os.path.join(TMP, "_sim_vecchio.py")
COMMIT_CURA = _cli_flag.sim_prima_del_flag(FLAGNOME, VECCHIO, radice=RADICE)
rr = braccio("prima", False, None, FIGLIO, sim=VECCHIO)
LOG.append("[prima] rc=%d %s  (il codice di prima e' %s^, e NON contiene %s)"
           % (rr.returncode, (rr.stdout or "").strip()[-150:], COMMIT_CURA[:8],
              FLAGNOME))
if rr.returncode:
    LOG.append((rr.stderr or "")[-1400:])
rr = braccio("mitosi", True, None, FIGLIO_MIT)
LOG.append("[mitosi] rc=%d %s" % (rr.returncode, (rr.stdout or "").strip()[-150:]))
if rr.returncode:
    LOG.append((rr.stderr or "")[-1400:])

P_ = []


def P(s=""):
    P_.append(s)


def crit(sigla, cosa, ok, detta):
    P("%-5s %-4s  %s" % (sigla, "PASS" if ok else "FAIL", cosa))
    for r_ in (detta or "").split(chr(10)):
        if r_:
            P("             " + r_)
    return bool(ok)


P("=" * 104)
P("SIGILLO `CURA 4` -- L'ACCENSIONE DEL CAMPO (`SEMINA_MATURA`)")
P("=" * 104)
P()
for l in LOG:
    P(l)
P()
if any("rc=1" in l for l in LOG):
    P("STOP: un braccio non e' arrivato in fondo. Nessun criterio si legge.")
    io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(P_) + chr(10))
    print(chr(10).join(P_))
    sys.exit(1)

OFF = leggi("off")
ON = leggi("on")
FZ = leggi("on_forzato")
MI = leggi("mitosi")
OK = []

P("CONFIGURAZIONE: TAU_A = %.1f   DT = %.3f   ->   TAU_A/DT = %.0f passi"
  % (OFF["TAU_A"], OFF["DT"], OFF["TAU_A"] / OFF["DT"]))
P("  scena (ii) (b), seme %d:  n = %d, archi = %d" % (SEME, OFF["n0"], OFF["archi0"]))
P()

# ---------------------------------------------------------------- A1
com = sorted(set(OFF["firme"]) & set(ON["firme"]))
sol_off = sorted(set(OFF["firme"]) - set(ON["firme"]))
sol_on = sorted(set(ON["firme"]) - set(OFF["firme"]))
diff = [k for k in com if OFF["firme"][k] != ON["firme"][k]]
# `A1` si legge fra il braccio OFF e il codice PRECEDENTE alla cura: qui si confronta OFF con
# ON al PASSO 1, che NON e' la byte-identita'. La byte-identita' vera e' OFF contro HEAD~.
P("NOTA SU `A1`: qui OFF e ON DEVONO differire (e' `A5`). La BYTE-IDENTITA' del ramo spento")
P("  si prova contro il codice PRECEDENTE alla cura, ed e' il braccio `A1` piu' sotto.")
P()

# ---------------------------------------------------------------- A1
PR = leggi("prima")
_comp = sorted(set(PR["firme"]) & set(OFF["firme"]))
_solo_pr = sorted(set(PR["firme"]) - set(OFF["firme"]))
_solo_off = sorted(set(OFF["firme"]) - set(PR["firme"]))
_dif1 = [k for k in _comp if PR["firme"][k] != OFF["firme"][k]]
OK.append(crit("A1", "flag SPENTO = BYTE-IDENTICO al codice PRECEDENTE (firma dei byte, un processo per braccio)",
               (not _dif1) and (not _solo_pr) and (not _solo_off),
               "campi confrontati %d   DIVERSI %d" % (len(_comp), len(_dif1))
               + chr(10) + "diversi: %s" % (", ".join(_dif1[:12]) or "NESSUNO")
               + chr(10) + "presenti solo nel VECCHIO: %s" % (_solo_pr or "nessuno")
               + chr(10) + "presenti solo nel NUOVO:   %s" % (_solo_off or "nessuno")
               + chr(10) + "(il vecchio e' %s^:soliton_simulator.py, estratto in "
               "BINARIO -- il PADRE del commit che ha introdotto %s, non `HEAD`: HEAD "
               "LA CONTIENE)" % (COMMIT_CURA[:8], FLAGNOME)))

# ---------------------------------------------------------------- CLI
# [`CLI-1`] **IL FLAG E' ARRIVATO DAL CLI, E NESSUNO L'HA ASSEGNATO A MANO.**
#   Sono DUE affermazioni, e servono entrambe: la prima si legge dallo stato del modulo
#   dopo `_cli()` + `_applica_flag(a)`; la seconda **si prova per AST sul SORGENTE DEI
#   FIGLI** (`STANDARD 9`: mai un `in` sul testo), perche' un'assegnazione rimessa
#   domani renderebbe il criterio di nuovo cieco.
_ast_ok, _ast_dove = True, []
for _nome_t, _tpl in (("FIGLIO", FIGLIO), ("FIGLIO_MIT", FIGLIO_MIT)):
    for _nd in ast.walk(ast.parse(_tpl)):
        if not isinstance(_nd, ast.Assign):
            continue
        for _tg in _nd.targets:
            if (isinstance(_tg, ast.Attribute) and isinstance(_tg.value, ast.Name)
                    and _tg.value.id == "S" and _tg.attr in (FLAGNOME, "SEMINA_LAM")):
                _ast_ok = False
                _ast_dove.append("%s:%d S.%s" % (_nome_t, _nd.lineno, _tg.attr))
_cli_att = [(n_, d_.get("CLI", {})) for n_, d_ in
            (("off", OFF), ("on", ON), ("on_forzato", FZ), ("mitosi", MI), ("prima", PR))]
_cli_ok = _ast_ok
for _n, _c in _cli_att:
    if _n == "prima":
        # il codice di PRIMA non ha il flag: l'atteso e' che sia ASSENTE, non False.
        # il codice di PRIMA non ha il flag: l'atteso e' ASSENTE, e l'opzione non e' nella
        # sua argv (`senza` la toglie prima, quindi NON compare fra le `scartate`).
        _cli_ok = _cli_ok and (_c.get("flag") == "ASSENTE")
        _cli_ok = _cli_ok and (_c.get("opz_nell_argv") is False)
    else:
        _cli_ok = _cli_ok and (bool(_c.get("flag")) == bool(_c.get("atteso")))
        _cli_ok = _cli_ok and (bool(_c.get("opz_nell_argv")) == bool(_c.get("atteso")))
        _cli_ok = _cli_ok and (_c.get("semina_lam") is True)
OK.append(crit("CLI", "il flag arriva DAL CLI (argv del driver) e NESSUN braccio lo assegna a mano",
               _cli_ok,
               (chr(10).join("%-11s flag=%-8s atteso=%-6s opz_nell_argv=%-6s "
                             "SEMINA_LAM=%-6s argv=%s scartate=%s"
                             % (_n, _c.get("flag"), _c.get("atteso"),
                                _c.get("opz_nell_argv"), _c.get("semina_lam"),
                                _c.get("argv_len"), _c.get("scartate"))
                             for _n, _c in _cli_att))
               + chr(10) + "argv CATTURATA dal driver: %d voci, e contiene %s"
               % (len(ARGV), OPZ)
               + chr(10) + ("nessuna assegnazione `S.%s`/`S.SEMINA_LAM` nei sorgenti dei "
                            "figli (verificato per AST)" % FLAGNOME if _ast_ok
                            else "ASSEGNAZIONI A MANO TROVATE: %s" % ", ".join(_ast_dove))))
P()

# ---------------------------------------------------------------- A2
OK.append(crit("A2", "al passo 1 `ramp == 1` su TUTTI i nodi della semina iniziale (ESATTO)",
               ON["ramp1_iniz_min"] == 1.0 and ON["ramp1_iniz_uguali_1"] == ON["n0"],
               "ON : min %.15f  max %.15f   uguali a 1: %d su %d"
               % (ON["ramp1_iniz_min"], ON["ramp1_iniz_max"], ON["ramp1_iniz_uguali_1"], ON["n0"])
               + chr(10) + "OFF: min %.15f  max %.15f   (il riferimento: oggi e' ~0)"
               % (OFF["ramp1_iniz_min"], OFF["ramp1_iniz_max"])
               + chr(10) + "e al passo ZERO la somma dei pesi: ON %.6e contro OFF %.6e"
               % (ON["pesi0_somma"], OFF["pesi0_somma"])))

# ---------------------------------------------------------------- A3
_ok3 = (MI.get("nuovi", 0) > 0
        and max(MI.get("ramp_nuovi_alla_nascita", [1.0])) == 0.0
        and MI.get("passi_per_ramp1", 0) > 0
        and MI.get("ramp_finale", 0.0) >= 1.0)
OK.append(crit("A3", "un nodo nato da MITOSI parte da `ramp = 0` e arriva a 1 nel suo TEMPO-LUCE",
               _ok3,
               "nodi nati dalla mitosi: %s   (tw forzato nella finestra DERIVATA: %.6f)"
               % (MI.get("nuovi"), MI.get("TW0", float("nan")))
               + chr(10) + "ramp alla nascita: %s   atteso 0" % MI.get("ramp_nuovi_alla_nascita")
               + chr(10) + "tempo-luce alla nascita: %s" % MI.get("tempo_luce_nuovi")
               + chr(10) + "passi per arrivare a ramp = 1: %s   (ramp finale %s)"
               % (MI.get("passi_per_ramp1"), MI.get("ramp_finale"))
               + chr(10) + "ATTESO ~ tempo_luce/DT = %s passi"
               % (("%.1f" % (np.median(MI["tempo_luce_nuovi"]) / OFF["DT"]))
                  if isinstance(MI.get("tempo_luce_nuovi"), list) else "?")))

# ---------------------------------------------------------------- A4
OK.append(crit("A4", "contrasto massa/vuoto e `Lam` al passo 1, contro `P2 = 27` e `P3 = 5`",
               ON["contrasto"] > 1.0 and ON["Lam"] > OFF["Lam"],
               "contrasto  ON %.4f   OFF %.4f      previsto P2 = 27  -> rapporto %.3f"
               % (ON["contrasto"], OFF["contrasto"], ON["contrasto"] / 27.0)
               + chr(10) + "Lam        ON %.6e   OFF %.6e   previsto P3 = 5   -> rapporto %.3e"
               % (ON["Lam"], OFF["Lam"], ON["Lam"] / 5.0)
               + chr(10) + "salita di `Lam` ON/OFF: x%.4g   <- IL CONTROLLO che la cura AGISCE"
               % (ON["Lam"] / OFF["Lam"] if OFF["Lam"] else float("inf"))
               + chr(10) + "I_massa ON %.6e   I_vuoto ON %.6e" % (ON["I_massa"], ON["I_vuoto"])))

# ---------------------------------------------------------------- A5
OK.append(crit("A5", "CONTROLLO POSITIVO: ON e OFF DEVONO differire al passo 1",
               len(diff) > 0,
               "campi confrontati %d   DIVERSI %d   presenti in uno solo: OFF %s / ON %s"
               % (len(com), len(diff), sol_off or "nessuno", sol_on or "nessuno")
               + chr(10) + "primi diversi: %s" % (", ".join(diff[:10]) or "NESSUNO")
               + chr(10) + "un sigillo che verifica solo la byte-identita' a OFF passerebbe su"
               + chr(10) + "codice MORTO (par.10.2): questo e' il criterio che lo esclude."))

# ---------------------------------------------------------------- A6
OK.append(crit("A6", "CASO CHE DEVE FALLIRE: con `maturi=False` forzato, `A2` da' FAIL",
               not (FZ["ramp1_iniz_min"] == 1.0 and FZ["ramp1_iniz_uguali_1"] == FZ["n0"]),
               "forzato: min %.15f   uguali a 1: %d su %d   -> `A2` %s"
               % (FZ["ramp1_iniz_min"], FZ["ramp1_iniz_uguali_1"], FZ["n0"],
                  "FALLISCE (giusto)" if FZ["ramp1_iniz_min"] != 1.0 else "PASSA (e non deve)")
               + chr(10) + "somma dei pesi al passo 0: %.6e   (col flag ON ma senza maturita')"
               % FZ["pesi0_somma"]
               + chr(10) + "se `A2` passasse qui, non starebbe guardando la MATURITA'."))

# ---------------------------------------------------------------- A7 (AST)
import ast as _ast

src = io.open(os.path.join(RADICE, "soliton_simulator.py"), encoding="utf-8").read()
arb = _ast.parse(src)
letture_pesi = []
for n in _ast.walk(arb):
    if isinstance(n, (_ast.FunctionDef,)) and n.name == "_pesi":
        for m in _ast.walk(n):
            if isinstance(m, _ast.Name) and m.id == "TAU_A":
                letture_pesi.append(m.lineno)
OK.append(crit("A7", "`TAU_A` NON e' piu' letto da `_pesi` -- dall'AST, non da un `grep`",
               not letture_pesi,
               "occorrenze di `TAU_A` dentro `_pesi`: %s" % (letture_pesi or "NESSUNA")
               + chr(10) + "il denominatore passa da `_tempo_rampa()`, che restituisce `TAU_A`"
               + chr(10) + "SOLO a flag spento: i due ruoli sono separati, e la separazione e'"
               + chr(10) + "verificata dove sta la legge, non dove sta il nome."))

P()
P("CONTATORI DELLA RAMPA (A8), braccio ON: %s" % (ON["g_rampa"] or "NESSUNO"))
P()
P("=" * 104)
P("ESITO: %d/%d PASS" % (sum(1 for x in OK if x), len(OK)))
P("=" * 104)
P()
P("COSA QUESTO SIGILLO *NON* DICE:")
P("  - `A1` (byte-identita' del ramo SPENTO contro il codice PRECEDENTE) e' un braccio a se',")
P("    perche' richiede di estrarre il blob precedente da git. E' nel sigillo `_a1_cura4.py`.")
P("  - `A3` gira su una rete da 60 nodi, non sulla scena: misura UN nodo, non una statistica.")
P("  - la MITOSI e' forzata (la soglia `3pi` e' irraggiungibile, `SCALE-TW`): senza forzarla")
P("    `A3` non avrebbe nulla da misurare, e va detto invece di far sembrare che scatti da se'.")
P("  - la rimisura di `|dx|/d` a campo maturo NON e' qui: e' il passo dopo.")


T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
sys.exit(0 if all(OK) else 1)
