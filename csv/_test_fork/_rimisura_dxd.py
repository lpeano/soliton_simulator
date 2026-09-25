# -*- coding: utf-8 -*-
"""**LA RIMISURA DI `|dx|/d` A CAMPO MATURO** *(chiesta da Luca, 2026-09-25)*.

> *«Poi RIMISURA `|dx|/d` a campo maturo: la forma del freno-legge `(1+tanh)` era decisa a
> campo spento.»*

**IL RIFERIMENTO, e va citato con il suo regime:** `V8`/`V9` dal giro corto di `CURA 2`
*(`csv/_test_fork/_cura2_corto/BILANCIO_d0.txt`, blob `49fc54d2`, `120` passi, seme `42`)*:

```
  verso        n            p50      p90      p99    p99.9      max   >0.5  >1  >2
  discese   60538734     0.0019   0.0239   0.0310   0.0344   0.0385    0    0   0
  salite    65192342     0.0024   0.0124   0.0241   0.0307   0.0531    0    0   0
```

**⚠ QUEL GIRO AVEVA `ramp <= 0.024`, cioè un PESO D'ARCO di `5.76e-04` del maturo.** La
conclusione *«la saturazione di `tanh` non si presenta MAI»* **è stata tratta a campo spento.**

**COME SI MISURA, senza toccare il simulatore:** si **avvolge `_smorza`** e si contano le coppie
`(dx, prima)` — **lo stesso involucro di `_g4_prova`**, non una formula nuova.
**DUE BRACCI, un processo per ciascuno** *(`STANDARD 1`)*: `SEMINA_MATURA` **ON** e **OFF**, stessa
scena, stesso seme. **L'unica differenza è il campo.**

**➕ E SI REGISTRA `E[x²]`, che `Z146` dichiarava MANCANTE:** *«la deriva di `piana` vale
`exp(N·E[x²]/2)`, e `E[x²]` NON È STATO REGISTRATO — i quantili non bastano a stimare una media
di quadrati»*. **Qui si somma `x²` a mano, e il numero esce.**

**IL CRITERIO È QUELLO DI `V8`, già scritto:** la saturazione di `1+tanh` morde a `x` di ordine
`1`. **Se a campo maturo il massimo resta sotto `0.5`, la forma regge; se lo supera, la decisione
va riaperta.**
"""
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
FUORI = os.path.join(_QUI, "_rimisura_dxd")
DEST = os.path.join(FUORI, "RIMISURA_dxd.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEME = 11
SEP = 4.0
PASSI = 120        # lo STESSO numero del riferimento, per confrontabilita'

FIGLIO = r'''
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sim_rx", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = True
S.SEMINA_MATURA = bool(FLAG)
# ❌❌ LA PRIMA CORSA NON HA RACCOLTO NESSUN CAMPIONE, E LA COLPA E' MIA: `_smorza` e' chiamata
#   da `_smp_chiudi` (`:4166`, il sito `d0_passo` del riferimento) SOLO con `SCALA_MIN_PASSO`
#   ACCESO, e nel sorgente e' `False`. **Il driver della campagna lo ha `on`** (`SCALAMINPASSO`),
#   quindi misurare con i default del sorgente **misura un sistema senza freno**.
#   E' lo stesso errore del par.9 sui run senza `--cs-dinamico`: la configurazione fa parte
#   della misura, e non si eredita dai default.
# `SCALA_MIN` resta SPENTO: il driver lo tiene `off` perche' **non e' una cura approvata**.
S.SCALA_MIN_PASSO = True
S.SCALA_MIN = False

# --- L'INVOLUCRO SU `_smorza`: si contano le coppie (dx, prima). Nessuna riga del simulatore. ---
ACC = {}


def _voce(et):
    if et not in ACC:
        ACC[et] = dict(n=0, somma=0.0, somma2=0.0, massimo=0.0, oltre05=0, oltre1=0, oltre2=0,
                       campioni=[])
    return ACC[et]


_orig = S.Rete._smorza


def _wrap(self, prima, dx, quale):
    _p = np.asarray(prima, float)
    _d = np.asarray(dx, float)
    if _p.size and _d.size and _p.shape == _d.shape:
        _den = np.maximum(np.abs(_p), 1e-300)
        _x = np.abs(_d) / _den
        for _et, _m in (("salite", _d > 0.0), ("discese", _d < 0.0)):
            if not np.any(_m):
                continue
            _xx = _x[_m]
            v = _voce(_et)
            v["n"] += int(_xx.size)
            v["somma"] += float(_xx.sum())
            v["somma2"] += float(np.sum(_xx * _xx))       # <- `E[x^2]`, che mancava
            v["massimo"] = max(v["massimo"], float(_xx.max()))
            v["oltre05"] += int(np.sum(_xx > 0.5))
            v["oltre1"] += int(np.sum(_xx > 1.0))
            v["oltre2"] += int(np.sum(_xx > 2.0))
            # un CAMPIONE per i quantili: uno su 512, cosi' la memoria resta finita e il
            # campionamento e' DICHIARATO invece di essere implicito.
            v["campioni"].extend(_xx[::512].tolist())
        # e la stessa cosa per il SOLO chiamante `d0_passo`, che e' quello del riferimento
        if quale == "d0_passo":
            for _et, _m in (("salite_d0passo", _d > 0.0), ("discese_d0passo", _d < 0.0)):
                if not np.any(_m):
                    continue
                _xx = _x[_m]
                v = _voce(_et)
                v["n"] += int(_xx.size); v["somma"] += float(_xx.sum())
                v["somma2"] += float(np.sum(_xx * _xx))
                v["massimo"] = max(v["massimo"], float(_xx.max()))
                v["oltre05"] += int(np.sum(_xx > 0.5))
                v["oltre1"] += int(np.sum(_xx > 1.0))
                v["oltre2"] += int(np.sum(_xx > 2.0))
                v["campioni"].extend(_xx[::512].tolist())
    return _orig(self, prima, dx, quale)


S.Rete._smorza = _wrap

S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False

# ============================================================================================
# ❌❌ `net.step()` NON E' UN PASSO. IL PASSO DEL DRIVER SONO **CINQUE** CHIAMATE:
#
#     scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()
#
#   *(`csv/_test_fork/_scena_video.py`, riga 37 e riga 394)*
#
# E NON E' UN DETTAGLIO: `_smp_chiudi` -- cioe' IL FRENO su `d0`, il sito `d0_passo` da cui
#   vengono i numeri di `V8`/`V9` -- vive DENTRO `memoria_hebbiana_moto`, e il suo commento lo
#   dice: *"`memoria_hebbiana_moto` e' l'ULTIMA chiamata del passo NEL DRIVER"*.
#   Con il solo `net.step()` **il freno non si chiude mai**, e la rimisura non raccoglieva
#   NESSUN CAMPIONE.
#
# ⚠ E TOCCA ANCHE LE ALTRE MIE MISURE DI OGGI: la traiettoria di `|tw|` di `SCALE-TW` e la
#   corsa sui triangoli girano su un ciclo INCOMPLETO. Si rifanno con questo, e si dichiara.
# ============================================================================================
def passo_pieno(S, net):
    """IL PASSO COMPLETO, nell'ordine del driver. UNA funzione, cosi' non ci sono due versioni."""
    S.scuoti_vuoto(net)
    net.step()
    net.mitosi()
    net.rilassa_disegno()
    net.memoria_hebbiana_moto()


S._semina_masse_coerenti()
net = S.net
n0, a0 = int(net.n), int(len(net.d))
d0_med0 = float(np.median(net.d0))
for k in range(PASSI):
    passo_pieno(S, net)
o = dict(FLAG=bool(FLAG), n0=n0, archi0=a0, n1=int(net.n), archi1=int(len(net.d)),
         d0_med_inizio=d0_med0, d0_med_fine=float(np.median(net.d0)), passi=int(PASSI))
_tr = net._tempo_rampa()
_r = np.minimum(1.0, np.asarray(net.eta, float) / _tr)
o["ramp_fine_p50"] = float(np.median(_r)); o["ramp_fine_min"] = float(_r.min())
net.calcola_psi()
I = np.asarray(net.intensita(), float)
o["Lam_fine"] = float(I.mean())
for et, v in ACC.items():
    c = np.asarray(v["campioni"], float)
    o[et] = dict(n=v["n"], media=(v["somma"] / v["n"] if v["n"] else float("nan")),
                 Ex2=(v["somma2"] / v["n"] if v["n"] else float("nan")),
                 massimo=v["massimo"], oltre05=v["oltre05"], oltre1=v["oltre1"],
                 oltre2=v["oltre2"], n_campioni=int(c.size),
                 p50=(float(np.percentile(c, 50)) if c.size else float("nan")),
                 p90=(float(np.percentile(c, 90)) if c.size else float("nan")),
                 p99=(float(np.percentile(c, 99)) if c.size else float("nan")),
                 p999=(float(np.percentile(c, 99.9)) if c.size else float("nan")))
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  n %d -> %d  passi %d  max|dx|/d %s"
      % (NOME, n0, net.n, PASSI,
         max([v["massimo"] for v in ACC.values()]) if ACC else "nessun campione"))
'''


def braccio(nome, flag):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nFLAG = %r\nPASSI = %d\n"
           % (RADICE, TMP, nome, SEME, SEP, flag, PASSI)) + FIGLIO
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.run([sys.executable, p], cwd=RADICE, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


LOG = []
for nome, flag in (("maturo", True), ("spento", False)):
    rr = braccio(nome, flag)
    LOG.append("[%s] rc=%d %s" % (nome, rr.returncode, (rr.stdout or "").strip()[-180:]))
    if rr.returncode:
        LOG.append((rr.stderr or "")[-1600:])

P_ = []


def P(s=""):
    P_.append(s)


P("=" * 112)
P("RIMISURA DI `|dx|/d` A CAMPO MATURO -- il numero che decide la forma del freno-legge")
P("=" * 112)
P()
for l in LOG:
    P(l)
P()
if any("rc=1" in l for l in LOG):
    P("STOP: un braccio non e' arrivato in fondo.")
    io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(P_) + chr(10))
    print(chr(10).join(P_))
    sys.exit(1)


def leggi(n):
    return json.loads(io.open(os.path.join(TMP, n + ".json"), encoding="utf-8").read())


M = leggi("maturo")
Sp = leggi("spento")

P("IL RIFERIMENTO (`V8`/`V9`, `CURA 2`, blob `49fc54d2`, 120 passi, seme 42) -- A CAMPO SPENTO:")
P("  discese   60538734   p50 0.0019  p90 0.0239  p99 0.0310  p999 0.0344  max 0.0385  >0.5 = 0")
P("  salite    65192342   p50 0.0024  p90 0.0124  p99 0.0241  p999 0.0307  max 0.0531  >0.5 = 0")
P()
P("LE DUE CORSE DI OGGI -- stessa scena (ii) (b), seme %d, %d passi, UN PROCESSO PER BRACCIO"
  % (SEME, PASSI))
P("  CONFIGURAZIONE DICHIARATA: `SCALA_MIN_PASSO = True` (come il driver), `SCALA_MIN = False`")
P("  (con i default del SORGENTE `SCALA_MIN_PASSO` e' False e `_smorza` NON viene chiamata:")
P("   la prima corsa non ha raccolto NIENTE, ed era un difetto della mia configurazione.)")
P("  braccio   n           archi        ramp finale p50   Lam finale      med d0 inizio -> fine")
for et, D in (("MATURO", M), ("SPENTO", Sp)):
    P("  %-9s %-11d %-12d %-17.6f %-15.6e %.6f -> %.6f"
      % (et, D["n1"], D["archi1"], D["ramp_fine_p50"], D["Lam_fine"],
         D["d0_med_inizio"], D["d0_med_fine"]))
P()
P("-" * 112)
P("LA DISTRIBUZIONE DI `|dx|/d`, per verso e per braccio")
P("-" * 112)
P("  %-9s %-16s %-12s %-10s %-10s %-10s %-10s %-10s %-9s %-7s"
  % ("braccio", "verso", "n", "p50", "p90", "p99", "p99.9", "MAX", "E[x^2]", ">0.5"))
righe = []
for et, D in (("MATURO", M), ("SPENTO", Sp)):
    for verso in ("discese", "salite", "discese_d0passo", "salite_d0passo"):
        v = D.get(verso)
        if not v:
            continue
        righe.append((et, verso, v))
        P("  %-9s %-16s %-12d %-10.4f %-10.4f %-10.4f %-10.4f %-10.4f %-9.3e %-7d"
          % (et, verso, v["n"], v["p50"], v["p90"], v["p99"], v["p999"], v["massimo"],
             v["Ex2"], v["oltre05"]))
P()
P("  (i quantili vengono da un CAMPIONE dichiarato: uno su 512. `n`, `MAX`, `E[x^2]` e le quote")
P("   sono su TUTTI i campioni, non sul sottocampione.)")
P()

# ---------------------------------------------------------------- il criterio di `V8`
# ! e qui `_` era usato SIA come variabile di ciclo SIA nel confronto: il secondo `_`
#   sovrascriveva il primo, quindi il filtro guardava il VERSO invece del braccio.
mx_m = max([v["massimo"] for e, _, v in righe if e == "MATURO"] or [float("nan")])
mx_s = max([v["massimo"] for e, _, v in righe if e == "SPENTO"] or [float("nan")])
o05 = sum(v["oltre05"] for e, _, v in righe if e == "MATURO")
o1 = sum(v["oltre1"] for e, _, v in righe if e == "MATURO")
o2 = sum(v["oltre2"] for e, _, v in righe if e == "MATURO")
P("=" * 112)
P("IL CRITERIO DI `V8`, gia' scritto: la saturazione di `1+tanh` morde a `x` di ordine 1.")
P("=" * 112)
P("  max |dx|/d  a campo MATURO = %.6f" % mx_m)
P("  max |dx|/d  a campo SPENTO = %.6f   (riferimento di CURA 2: 0.0531)" % mx_s)
P("  rapporto MATURO/SPENTO = %.4f" % (mx_m / mx_s if mx_s else float("nan")))
P("  campioni oltre 0.5: %d      oltre 1: %d      oltre 2: %d   (braccio MATURO)"
  % (o05, o1, o2))
P()
# ❌ IL VERDETTO SU `nan` ERA VACUO, ed e' lo SPECCHIO del PASS su `inf` di `S9`:
#   `nan < 0.5` e' False, quindi la prima stesura stampava "IL MASSIMO SUPERA 0.5: LA DECISIONE
#   VA RIAPERTA" **quando non c'era NESSUN CAMPIONE**. Un FAIL vacuo su dati assenti costa come
#   un PASS vacuo: si porta dietro una diagnosi che non c'e'.
_tot = sum(v["n"] for _, _, v in righe)
if not righe or not np.isfinite(mx_m) or _tot == 0:
    P("  -> ** NON MISURATO: NESSUN CAMPIONE. ** `_smorza` non e' stata chiamata con forme")
    P("     compatibili, oppure il freno era SPENTO. Non si legge nulla, e in particolare")
    P("     **NON si conclude che il massimo superi 0.5**: non c'e' un massimo.")
    P("     (campioni totali: %d)" % _tot)
elif mx_m < 0.5:
    P("  -> LA FORMA `1+tanh` REGGE ANCHE A CAMPO MATURO: il massimo resta sotto 0.5, cioe'")
    P("     la saturazione non morde. **La decisione di Luca NON va riaperta per questo motivo.**")
else:
    P("  -> ** IL MASSIMO SUPERA 0.5 A CAMPO MATURO: LA DECISIONE VA RIAPERTA. **")
    P("     La conclusione \"la saturazione non si presenta MAI\" era vera A CAMPO SPENTO.")
P()
P("E `E[x^2]`, CHE `Z146` DICHIARAVA MANCANTE (la deriva di `piana` vale `exp(N*E[x^2]/2)`):")
for et, verso, v in righe:
    if verso in ("salite", "discese"):
        P("  %-9s %-9s  E[x^2] = %.6e   n = %d   ->  N*E[x^2]/2 = %.6e"
          % (et, verso, v["Ex2"], v["n"], v["n"] * v["Ex2"] / 2.0))
P("  (e' il numero che mancava sull'altro piatto del confronto: ora c'e'.)")
P()
P("COSA QUESTO NON DICE:")
P("  - UN SEME. Non e' una barra d'errore (par.0-ter `P3`: servono >= 4 semi).")
P("  - la scena e' la (ii) (b), NON quella di `CURA 2`: il riferimento `0.0531` viene da una")
P("    scena DIVERSA, quindi il confronto MATURO/SPENTO di oggi (stessa scena, stesso seme) e'")
P("    quello che attribuisce, e il `0.0531` sta qui come STORIA.")
P("  - `120` passi: lo stesso numero del riferimento, per confrontabilita'.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
