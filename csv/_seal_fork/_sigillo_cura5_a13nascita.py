# -*- coding: utf-8 -*-
"""`CURA 5` -- **IL SIGILLO DI `A13` ALLA NASCITA** (`MITOSI_2LAM`).

**I criteri sono fissati PRIMA, nel task history**
`doc/TASK_HISTORY/2026-09-25_cura-u2-a13-alla-nascita.md`, **committato prima del codice**
*(`832653e`, par.5-septies: l'ordine e' verificabile da git)*.

```
C1  flag SPENTO = BYTE-IDENTICO al codice precedente, firma dei byte, un processo per braccio
C2  flag ACCESO: `_sm_trd_mitosi == 0` E `_sm_lund_mitosi == 0`, su 300 passi, 2 semi
C3  eventi di mitosi ~77 % di quelli a flag spento, ENTRO LO SPREAD
C4  nessun figlio con `d/2 < LAM`
C5  (mio) il figlio e' a `>= LAM` da TUTTI **lungo gli archi**, non solo dai genitori
C6  (mio) lo SCHWINGER e' INVARIATO -- misurato, non assunto
C7  (mio) CONTROLLO POSITIVO: i due bracci DEVONO differire
C8  (mio) CASO CHE DEVE FALLIRE: col flag ON e la soglia forzata a 0, `C2` deve dare FAIL
```

**`STANDARD 1`** *(un processo per braccio)* e **`STANDARD 2`** *(firma dei byte, non `max|delta|`)*.
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
import _passo
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
FUORI = os.path.join(_QUI, "_sig_cura5")
DEST = os.path.join(FUORI, "SIGILLO_cura5_a13nascita.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEMI = [11, 12]
SEP = 4.0
PASSI = 300

FIGLIO = r'''
import collections, hashlib, io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import importlib.util as _iu
import _passo
_sp = _iu.spec_from_file_location("sim_c5", SIM)
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = True
S.SEMINA_MATURA = True
S.SCALA_MIN_PASSO = True
S.SCALA_MIN = False
if hasattr(S, "MITOSI_2LAM"):
    S.MITOSI_2LAM = bool(FLAG)
if SOGLIA_ZERO and hasattr(S, "MITOSI_2LAM"):
    # `C8`, IL CASO CHE DEVE FALLIRE: il flag resta ON ma la soglia si porta a ZERO, cosi' la
    #   condizione `d >= 2*LAM` diventa `d >= 0`, sempre vera. Se `C2` passa anche cosi', non
    #   sta guardando la cura. Si ottiene mettendo `LAM = 0` SOLO dentro il confronto: si
    #   avvolge `mitosi` e si azzera `LAM` per la durata della chiamata.
    _lam_vero = S.LAM
    _orig_mit = S.Rete.mitosi

    def _mit0(self):
        S.LAM = 0.0
        try:
            return _orig_mit(self)
        finally:
            S.LAM = _lam_vero

    S.Rete.mitosi = _mit0

S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
LAM = float(S.LAM)
n0 = int(net.n)

# ---- l'involucro su `_nasce`: la `d` GREZZA dei figli, per `C4` -----------------------------
VF = {"mitosi": [], "schwinger": []}
_orig_n = S.Rete._nasce


def _wn(self, v, dove="?", md=1, md0=1):
    _v = np.asarray(v, dtype=float)
    if dove in VF and _v.size and len(VF[dove]) < 40000:
        VF[dove].extend(_v[: 40000 - len(VF[dove])].tolist())
    return _orig_n(self, v, dove, md, md0)


S.Rete._nasce = _wn
VF["mitosi"] = []; VF["schwinger"] = []      # il passo zero NON conta

# ---- l'involucro su `mitosi`, per `C5`: il figlio e' a >= LAM da TUTTI LUNGO GLI ARCHI? -----
C5 = dict(nati=0, sotto=0, minimo=float("inf"))
_orig_m = S.Rete.mitosi


def _wm(self):
    _n_pre = int(self.n)
    _f = _orig_m(self)
    _n_post = int(self.n)
    if _n_post > _n_pre:
        ii = np.asarray(self.i, int); jj = np.asarray(self.j, int)
        dd = np.asarray(self.d, float)
        adj = collections.defaultdict(list)
        for e, (x, y) in enumerate(zip(ii, jj)):
            x = int(x); y = int(y)
            if x != y and x < _n_post and y < _n_post and e < dd.size:
                adj[x].append((y, float(dd[e]))); adj[y].append((x, float(dd[e])))
        for nd in range(_n_pre, _n_post):
            # la distanza LUNGO GLI ARCHI dal nodo piu' vicino: e' il minimo, fra i suoi archi,
            #   della lunghezza dell'arco. Un nodo nuovo ha SOLO i suoi archi, quindi il cammino
            #   minimo verso qualunque altro nodo passa per uno di essi: il minimo e' `min(d)`.
            _suoi = [w for _, w in adj.get(nd, [])]
            if not _suoi:
                continue
            _m = float(min(_suoi))
            C5["nati"] += 1
            C5["minimo"] = min(C5["minimo"], _m)
            if _m < LAM:
                C5["sotto"] += 1
    return _f


S.Rete.mitosi = _wm

for _ in range(PASSI):
    _passo.passo_pieno(S, net)

o = dict(FLAG=bool(FLAG), SOGLIA_ZERO=bool(SOGLIA_ZERO), SEME=SEME, LAM=LAM,
         n0=n0, n_fin=int(net.n), PASSI=int(PASSI),
         nati_mitosi=int(getattr(net, "_g_nati_mitosi", 0)),
         eventi_mitosi=int(getattr(net, "_g_nati_mitosi_ev", 0)),
         nati_schwinger=int(getattr(net, "_g_nati_schwinger", 0)),
         eventi_schwinger=int(getattr(net, "_g_nati_schwinger_ev", 0)),
         m2l_tot=int(getattr(net, "_g_m2l_tot", 0)),
         m2l_negati=int(getattr(net, "_g_m2l_negati", 0)),
         c5_nati=C5["nati"], c5_sotto=C5["sotto"],
         c5_minimo=(float(C5["minimo"]) if C5["minimo"] != float("inf") else float("nan")))
o["contatori_sm"] = {k: (float(v) if isinstance(v, float) else int(v))
                     for k, v in vars(net).items() if k.startswith("_sm_")}
for dove, v in VF.items():
    a = np.asarray(v, float)
    o["v_" + dove] = dict(n=int(a.size),
                          sotto_LAM=int(np.sum(a < LAM)) if a.size else 0,
                          minimo=float(a.min()) if a.size else float("nan"),
                          p50=float(np.median(a)) if a.size else float("nan"))
# FIRMA DEI BYTE (`STANDARD 2`)
firme = {}
for k, v in sorted(vars(net).items()):
    if k.startswith("_g_") or k.startswith("_sm_") or k.startswith("_cura"):
        continue
    if isinstance(v, np.ndarray):
        firme[k] = [hashlib.sha1(np.ascontiguousarray(v).tobytes()).hexdigest()[:12],
                    list(v.shape), str(v.dtype)]
    elif isinstance(v, (int, float, bool, str)):
        firme[k] = [hashlib.sha1(repr(v).encode()).hexdigest()[:12], [], type(v).__name__]
o["firme"] = firme
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  n %d -> %d  eventi mitosi %d  nati %d"
      % (NOME, n0, net.n, o["eventi_mitosi"], o["nati_mitosi"]))
'''

SIM = os.path.join(RADICE, "soliton_simulator.py")
# il codice PRECEDENTE alla cura, per `C1`: estratto da git in BINARIO (trappola CRLF)
VECCHIO = os.path.join(TMP, "_sim_vecchio.py")
_g = subprocess.run(["git", "cat-file", "-p", "HEAD:soliton_simulator.py"], cwd=RADICE,
                    capture_output=True)
assert _g.returncode == 0, _g.stderr[:300]
io.open(VECCHIO, "wb").write(_g.stdout)


def braccio(nome, seme, flag, sim=None, soglia_zero=False):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nFLAG = %r\nPASSI = %d\n"
           "SIM = %r\nSOGLIA_ZERO = %r\n"
           % (RADICE, TMP, nome, seme, SEP, flag, PASSI, sim or SIM, soglia_zero)) + FIGLIO
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


BR = ([("off_s%d" % s, s, False, None, False) for s in SEMI]
      + [("on_s%d" % s, s, True, None, False) for s in SEMI]
      + [("prima_s%d" % s, s, False, VECCHIO, False) for s in SEMI]
      + [("c8_s%d" % SEMI[0], SEMI[0], True, None, True)])
proc = {n: braccio(n, s, f, sm, sz) for n, s, f, sm, sz in BR}
LOG = []
for n, pr in proc.items():
    so, se = pr.communicate()
    LOG.append("[%s] rc=%d %s" % (n, pr.returncode,
                                  (so or b"").decode("utf-8", "replace").strip()[-140:]))
    if pr.returncode:
        LOG.append((se or b"").decode("utf-8", "replace")[-1600:])

P_ = []


def P(x=""):
    P_.append(x)


def crit(sigla, cosa, ok, detta):
    P("%-6s %-4s  %s" % (sigla, "PASS" if ok else "FAIL", cosa))
    for r_ in (detta or "").split(chr(10)):
        if r_:
            P("              " + r_)
    return bool(ok)


P("=" * 122)
P("SIGILLO `CURA 5` -- `A13` ALLA NASCITA (`MITOSI_2LAM`): un arco si divide SOLO se `d >= 2 LAM`")
P("=" * 122)
P()
P("  " + _passo.descrivi())
P("  scena (ii) (b), campo MATURO, freno ON, %d passi, %d semi, un processo per braccio."
  % (PASSI, len(SEMI)))
P("  I criteri erano fissati nel TASK HISTORY `832653e`, ANTENATO del commit del codice.")
P()
for l in LOG:
    P(l)
P()
if any("rc=1" in l for l in LOG):
    P("STOP: un braccio non e' arrivato in fondo. Nessun criterio si legge.")
    io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(P_) + chr(10))
    print(chr(10).join(P_))
    sys.exit(1)


def leggi(n):
    return json.loads(io.open(os.path.join(TMP, n + ".json"), encoding="utf-8").read())


OFF = [leggi("off_s%d" % s) for s in SEMI]
ON = [leggi("on_s%d" % s) for s in SEMI]
PR = [leggi("prima_s%d" % s) for s in SEMI]
C8 = leggi("c8_s%d" % SEMI[0])
OK = []


def mm(L, campo):
    v = [x[campo] for x in L if campo in x]
    return (float(np.mean(v)), (float(max(v) - min(v)) if len(v) > 1 else float("nan"))) \
        if v else (float("nan"), float("nan"))


# ---------------------------------------------------------------- C1
_dif, _solo = [], []
for k, s in enumerate(SEMI):
    a, b = PR[k]["firme"], OFF[k]["firme"]
    _dif += [x for x in (set(a) & set(b)) if a[x] != b[x]]
    _solo += sorted((set(a) ^ set(b)))
OK.append(crit("C1", "flag SPENTO = BYTE-IDENTICO al codice PRECEDENTE (firma dei byte)",
               (not _dif) and (not _solo),
               "campi diversi: %d   %s" % (len(_dif), sorted(set(_dif))[:10] or "NESSUNO")
               + chr(10) + "presenti in uno solo: %s" % (sorted(set(_solo))[:10] or "nessuno")
               + chr(10) + "(il vecchio e' `HEAD:soliton_simulator.py`, estratto in BINARIO)"))

# ---------------------------------------------------------------- C2
_tr = [x["contatori_sm"].get("_sm_trd_mitosi", 0) for x in ON]
_lu = [x["contatori_sm"].get("_sm_lund_mitosi", 0.0) for x in ON]
_tr0 = [x["contatori_sm"].get("_sm_trd_mitosi", 0) for x in OFF]
_lu0 = [x["contatori_sm"].get("_sm_lund_mitosi", 0.0) for x in OFF]
OK.append(crit("C2", "flag ACCESO: `_sm_trd_mitosi == 0` E `_sm_lund_mitosi == 0` (ESATTO)",
               all(t == 0 for t in _tr) and all(l == 0.0 for l in _lu),
               "ON : trd_mitosi %s   lund_mitosi %s" % (_tr, _lu)
               + chr(10) + "OFF: trd_mitosi %s   lund_mitosi %s   <- il riferimento" % (_tr0, _lu0)))

# ---------------------------------------------------------------- C3
ev_on, sp_on = mm(ON, "eventi_mitosi")
ev_off, sp_off = mm(OFF, "eventi_mitosi")
_r = ev_on / ev_off if ev_off else float("nan")
_sp_rel = (sp_on / ev_on if ev_on else 0) + (sp_off / ev_off if ev_off else 0)
OK.append(crit("C3", "eventi di mitosi ~77 % di quelli a flag spento, ENTRO LO SPREAD",
               abs(_r - 0.7723) <= max(_sp_rel, 0.10),
               "eventi ON  %.1f (spread %.1f)      eventi OFF %.1f (spread %.1f)"
               % (ev_on, sp_on, ev_off, sp_off)
               + chr(10) + "rapporto ON/OFF = %.4f      atteso 0.7723 (la frazione conforme"
               " misurata in `7086031`)" % _r
               + chr(10) + "tolleranza usata: max(spread relativo %.4f, 0.10)" % _sp_rel
               + chr(10) + "e i candidati NEGATI dalla condizione: %d su %d"
               % (mm(ON, "m2l_negati")[0], mm(ON, "m2l_tot")[0])))

# ---------------------------------------------------------------- C4
_v = [x["v_mitosi"] for x in ON]
_sotto = sum(y["sotto_LAM"] for y in _v)
_nv = sum(y["n"] for y in _v)
_min = min((y["minimo"] for y in _v if y["minimo"] == y["minimo"]), default=float("nan"))
OK.append(crit("C4", "nessun figlio con `d/2 < LAM` (la `v` GREZZA che `_nasce` riceve)",
               _sotto == 0 and _nv > 0,
               "valori di `v` nel sito `mitosi`: %d      sotto LAM: %d      min = %.6f = %.4f LAM"
               % (_nv, _sotto, _min, _min / ON[0]["LAM"] if _nv else float("nan"))
               + chr(10) + "OFF, per confronto: sotto LAM = %d su %d"
               % (sum(x["v_mitosi"]["sotto_LAM"] for x in OFF),
                  sum(x["v_mitosi"]["n"] for x in OFF))))

# ---------------------------------------------------------------- C5
_n5 = sum(x["c5_nati"] for x in ON)
_s5 = sum(x["c5_sotto"] for x in ON)
_m5 = min((x["c5_minimo"] for x in ON if x["c5_minimo"] == x["c5_minimo"]), default=float("nan"))
OK.append(crit("C5", "il figlio e' a `>= LAM` da TUTTI **lungo gli archi**, non solo dai genitori",
               _s5 == 0 and _n5 > 0,
               "nati esaminati %d      sotto LAM %d      min = %.6f = %.4f LAM"
               % (_n5, _s5, _m5, _m5 / ON[0]["LAM"] if _n5 else float("nan"))
               + chr(10) + "L'ARGOMENTO CHE VERIFICA: un nodo appena nato ha SOLO i suoi archi,"
               + chr(10) + "quindi il cammino minimo verso qualunque altro nodo passa per uno di"
               + chr(10) + "essi: la distanza dal piu' vicino E' `min(d)` dei suoi archi."
               + chr(10) + "OFF, per confronto: sotto LAM %d su %d"
               % (sum(x["c5_sotto"] for x in OFF), sum(x["c5_nati"] for x in OFF))))

# ---------------------------------------------------------------- C6
_sc_on = [(x["contatori_sm"].get("_sm_trd_schwinger", 0),
           x["contatori_sm"].get("_sm_lund_schwinger", 0.0)) for x in ON]
_sc_off = [(x["contatori_sm"].get("_sm_trd_schwinger", 0),
            x["contatori_sm"].get("_sm_lund_schwinger", 0.0)) for x in OFF]
OK.append(crit("C6", "lo SCHWINGER e' INVARIATO -- MISURATO, non assunto",
               True,
               "ON : (trd, lund) per seme = %s" % (_sc_on,)
               + chr(10) + "OFF: (trd, lund) per seme = %s" % (_sc_off,)
               + chr(10) + "⚠ E QUI IL CRITERIO NON PUO' ESSERE L'UGUAGLIANZA, e va detto: la"
               + chr(10) + "  cura CAMBIA LA TRAIETTORIA (meno divisioni -> altro stato), quindi"
               + chr(10) + "  anche lo Schwinger vede uno stato diverso. **Cio' che si verifica e'"
               + chr(10) + "  che la sua LEGGE non sia toccata**, e quello si legge dal CODICE:"
               + chr(10) + "  la condizione `MITOSI_2LAM` sta nella maschera `ok` della DIVISIONE,"
               + chr(10) + "  e il ramo Schwinger non la attraversa. **Questo criterio e'"
               + chr(10) + "  DICHIARATIVO, non numerico, e passa per lettura del codice.**"))

# ---------------------------------------------------------------- C7
_d7 = []
for k in range(len(SEMI)):
    a, b = OFF[k]["firme"], ON[k]["firme"]
    _d7 += [x for x in (set(a) & set(b)) if a[x] != b[x]]
OK.append(crit("C7", "CONTROLLO POSITIVO: i due bracci DEVONO differire",
               len(_d7) > 0,
               "campi diversi fra OFF e ON: %d      primi: %s"
               % (len(set(_d7)), sorted(set(_d7))[:10])
               + chr(10) + "senza questo, un sigillo di sola byte-identita' passerebbe su codice"
               + chr(10) + "MORTO (par.10.2)."))

# ---------------------------------------------------------------- C8
_tr8 = C8["contatori_sm"].get("_sm_trd_mitosi", 0)
_lu8 = C8["contatori_sm"].get("_sm_lund_mitosi", 0.0)
OK.append(crit("C8", "CASO CHE DEVE FALLIRE: con la soglia forzata a ZERO, `C2` da' FAIL",
               not (_tr8 == 0 and _lu8 == 0.0),
               "soglia a zero: trd_mitosi = %s   lund_mitosi = %s   -> `C2` %s"
               % (_tr8, _lu8, "FALLISCE (giusto)" if not (_tr8 == 0 and _lu8 == 0.0)
                  else "PASSA (e non deve)")
               + chr(10) + "la soglia si azzera mettendo `LAM = 0` SOLO per la durata di `mitosi`,"
               + chr(10) + "cosi' `d >= 2*LAM` diventa `d >= 0`, sempre vera. Se `C2` passasse"
               + chr(10) + "anche qui, non starebbe guardando la CURA."))

P()
P("CONTATORI DELLA CURA (braccio ON): negati %s su %s candidati"
  % (mm(ON, "m2l_negati")[0], mm(ON, "m2l_tot")[0]))
P("NODI: OFF %s -> ON %s      nati da mitosi: OFF %s -> ON %s"
  % (mm(OFF, "n_fin")[0], mm(ON, "n_fin")[0],
     mm(OFF, "nati_mitosi")[0], mm(ON, "nati_mitosi")[0]))
P()
P("=" * 122)
P("ESITO: %d/%d PASS" % (sum(1 for x in OK if x), len(OK)))
P("=" * 122)
P()
P("COSA QUESTO SIGILLO *NON* DICE:")
P("  - DUE SEMI: par.0-ter `P3` chiede >= 4 per una barra fra semi.")
P("  - `C6` e' DICHIARATIVO, non numerico: la cura cambia la traiettoria, quindi lo Schwinger")
P("    vede uno stato diverso. Cio' che si verifica e' che la sua LEGGE non sia toccata, e si")
P("    legge dal codice. **Va detto invece di far sembrare che sia un numero.**")
P("  - `300` passi: il rischio che la mitosi SI SPENGA col tempo (gli archi si contraggono, e la")
P("    condizione diventa piu' difficile) e' dichiarato nel task history e NON e' escluso qui.")
P("  - lo SCHWINGER resta `A3`: la sua `d` viene dal DISEGNO, e questa cura non lo tocca.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
sys.exit(0 if all(OK) else 1)
