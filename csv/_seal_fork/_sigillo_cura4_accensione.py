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
import io
import json
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
FUORI = os.path.join(_QUI, "_sig_cura4")
DEST = os.path.join(FUORI, "SIGILLO_cura4_accensione.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEME = 11
SEP = 4.0          # la scena (ii) (b): la piu' economica

FIGLIO = r'''
import hashlib, io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sim_c4", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = True
S.SEMINA_MATURA = bool(FLAG)
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

o = dict(FLAG=bool(FLAG), MATURI_FORZATO=MATURI_FORZATO, n0=n0, archi0=int(len(net.d)),
         TAU_A=float(S.TAU_A), DT=float(S.DT))

def _ramp(net):
    _tr = net._tempo_rampa()
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
o["g_rampa"] = {k: (list(v) if isinstance(v, tuple) else v)
                for k, v in vars(net).items() if k.startswith("_g_rampa") or k.startswith("_g_cura4")}

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
_sp = _iu.spec_from_file_location("sim_c4m", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)
S.SEMINA_MATURA = True
net = S.Rete(7)
net.semina(60)                # rete piccola: `A3` misura UN nodo, non una statistica
net.step()                    # senza, `_rho_sorgente()` e' vuoto e `mitosi` si SCHIANTA (FRAG1)
n_pre = int(net.n)
# LA FINESTRA DI CREAZIONE SI DERIVA DAL CODICE (par.9), non si sceglie:
_s0 = (S.PHI_CRIT + np.pi) if (S.TORS_4PI and not S.FASE_2PI) else S.PHI_CRIT
_centro = 0.5 * ((1.0 + _s0 / S.PHI_CRIT) + (1.0 + (4.0 * np.pi) / S.PHI_CRIT))
TW0 = 0.5 * (_s0 + (_centro - 1.0) * S.PHI_CRIT)
net.tw = np.zeros(len(net.d)); net.tw[0] = TW0
_rng = net.rng
class _R:
    def __getattr__(self, k): return getattr(_rng, k)
    def random(self, *a, **k):
        _n = a[0] if a else k.get("size")
        return np.zeros(_n) if _n is not None else 0.0
net.rng = _R()
net.mitosi()
nuovi = np.arange(n_pre, net.n)
o = dict(n_pre=n_pre, n_post=int(net.n), nuovi=int(nuovi.size), TW0=float(TW0))
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
io.open(os.path.join(TMPD, "mitosi.json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK mitosi  n %d -> %d  nuovi %d" % (n_pre, net.n, nuovi.size))
'''


def braccio(nome, flag, maturi=None, sorgente=FIGLIO):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nFLAG = %r\nMATURI_FORZATO = %r\n"
           % (RADICE, TMP, nome, SEME, SEP, flag, maturi)) + sorgente
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.run([sys.executable, p], cwd=RADICE, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def leggi(nome):
    return json.loads(io.open(os.path.join(TMP, nome + ".json"), encoding="utf-8").read())


LOG = []
BR = [("off", False, None), ("on", True, None), ("on_forzato", True, False)]
for nome, flag, mat in BR:
    rr = braccio(nome, flag, mat)
    LOG.append("[%s] rc=%d %s" % (nome, rr.returncode, (rr.stdout or "").strip()[-150:]))
    if rr.returncode:
        LOG.append((rr.stderr or "")[-1400:])
# `A1`: il ramo SPENTO contro il codice PRECEDENTE alla cura. Il blob si estrae da git in
# BINARIO (la trappola CRLF del par.5-quinquies), e il braccio gira su QUEL file.
VECCHIO = os.path.join(TMP, "_sim_vecchio.py")
_g = subprocess.run(["git", "cat-file", "-p", "HEAD:soliton_simulator.py"], cwd=RADICE,
                    capture_output=True)
assert _g.returncode == 0, _g.stderr[:300]
io.open(VECCHIO, "wb").write(_g.stdout)


def braccio_vecchio(nome):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nFLAG = %r\n"
           "MATURI_FORZATO = %r\nSIMV = %r\n"
           % (RADICE, TMP, nome, SEME, SEP, False, None, VECCHIO)) + FIGLIO.replace(
        'os.path.join(RAD, "soliton_simulator.py")', "SIMV").replace(
        "S.SEMINA_MATURA = bool(FLAG)",
        "if hasattr(S, 'SEMINA_MATURA'): S.SEMINA_MATURA = bool(FLAG)")
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.run([sys.executable, p], cwd=RADICE, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


rr = braccio_vecchio("prima")
LOG.append("[prima] rc=%d %s" % (rr.returncode, (rr.stdout or "").strip()[-150:]))
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
               + chr(10) + "(il vecchio e' `HEAD:soliton_simulator.py`, estratto in BINARIO)"))

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
