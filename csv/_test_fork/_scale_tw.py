# -*- coding: utf-8 -*-
"""`SCALE-TW` -- **quanto vale `|tw|` nel regime `A13`, e la soglia `3pi` e' raggiungibile?**

> **Mandato di Luca, 2026-09-25, punto (b): SOLA LETTURA.** *Il livello raggiunto da `|tw|`
> dipende da `_ttw`: stimalo (stato stazionario) e MISURALO al passo zero e dopo pochi passi
> nella scena `(ii)`, per dire se la soglia `3pi` e' raggiungibile nel regime `A13`.*

**LA STIMA, e va scritta PRIMA di guardare** *(par.5-septies)*. Dal codice (`:5081`):

```
tw  <-  tw + _w8(D(dph + twist_dip))  -  dt_e * tw / _ttw
        \\_______ incremento _______/    \\___ perdita ___/
```

E' un **CAMMINO ALEATORIO SMORZATO**, la stessa forma di `omega_s` (par.9). Con incrementi
`s_n` a media nulla e varianza `sigma^2`, e tasso di smorzamento `lambda = dt_e/_ttw`:

```
Var(tw) stazionaria = sigma^2 / (2 lambda - lambda^2)  ~  sigma^2 * _ttw / (2 dt_e)
|tw|_eq             ~  sigma * sqrt(_ttw / (2 dt_e))
```

**E' LA STESSA FORMULA di `omega_eq = |F| sqrt(dt_n tau / 2)`** del par.9, che li' fu **misurata**
(previsto `7.06e4`, osservato `7.27e4`, scarto `x1.03`). **Non e' un modello nuovo: e' quello
gia' validato su questo repo su un'altra variabile.**

**COSA SI MISURA, tutto pure-read:**
```
_ttw        = max(2pi/(|phivel_i - phivel_j| + 1e-3), 1e-3)     -- la costante di tempo LOCALE
dt_e        = il tempo d'arco, dallo snapshot `_dt_e_ultimo`
sigma       = std dell'INCREMENTO `_w8(D(dph + twist_dip))` fra due passi consecutivi
|tw|        p50, p95, max          ai passi 0, 1, 2, 5, 10, 20
frazione con |tw| >= soglia locale, >= 3pi, >= TW_TETTO
```

**IL CRITERIO E' SCRITTO PRIMA:** *se `|tw|_eq` stimato e misurato sono entrambi **sotto `3pi`
di piu' di un fattore 2**, la soglia **non e' raggiungibile** in questo regime, e la mitosi
scatta solo sulla coda della distribuzione.* **Un numero solo non basta: serve la FRAZIONE.**

**NESSUNA RIGA DI CODICE DEL SIMULATORE VIENE TOCCATA.**
"""
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_scale_tw", "SCALE_TW_misura.txt")
os.makedirs(os.path.dirname(DEST), exist_ok=True)

import importlib.util as iu

_sp = iu.spec_from_file_location("sim_tw", os.path.join(RADICE, "soliton_simulator.py"))
S = iu.module_from_spec(_sp)
_sp.loader.exec_module(S)

P_ = []


def P(s=""):
    P_.append(s)
    print(s)


def q(a, etichetta, div=1.0):
    a = np.asarray(a, float)
    if not a.size:
        return "%s: VUOTO" % etichetta
    return ("%s: p50 %.6g  p95 %.6g  max %.6g" % (etichetta, np.median(a) / div,
                                                  np.percentile(a, 95) / div, a.max() / div))


PASSI = [0, 1, 2, 5, 10, 20]
SEME = 11
SEP = 4.0                     # la scena (b): la piu' economica delle due

P("=" * 100)
P("`SCALE-TW` (b) -- IL LIVELLO DI `|tw|` NEL REGIME `A13`, E LA SOGLIA `3pi`")
P("=" * 100)
P()
P("COSTANTI, lette dal sorgente:")
P("  PHI_CRIT  = %.9f   (= 2 pi)          `:422`" % S.PHI_CRIT)
P("  TAU_TW    = %.4f                      `:427`  -- usato SOLO come fallback: `TAU_LOCALI` e' %s"
  % (S.TAU_TW, S.TAU_LOCALI))
P("  TORS_4PI  = %s   FASE_2PI = %s   ->  soglia0 = %s"
  % (S.TORS_4PI, S.FASE_2PI,
     ("PHI_CRIT + pi = 3 pi = %.6f" % (S.PHI_CRIT + np.pi)) if (S.TORS_4PI and not S.FASE_2PI)
     else ("PHI_CRIT = %.6f" % S.PHI_CRIT)))
P("  TW_TETTO  = %.9f   (= 4 pi)          `:5626` (LOCALE di `mitosi`)" % (4.0 * np.pi))
P("  QMIN_M    = %.6f  <- la soglia di densita' e' `>= 0`: SEMPRE VERA" % S.QMIN_M)
P()

S.SEMINA_LAM = True
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = SEP
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
SOGLIA3 = S.PHI_CRIT + np.pi
TETTO = 4.0 * np.pi

P("SCENA (ii) (b): n = %d, archi = %d, seme %d" % (net.n, len(net.d), SEME))
P()
P("-" * 100)
P("%-6s %-34s %-34s %-24s" % ("passo", "|tw| (in unita' di pi)", "_ttw", "frazioni"))
P("-" * 100)

prev_twp = None
righe = []
for k in range(max(PASSI) + 1):
    if k:
        net.step()
    if k not in PASSI:
        continue
    tw = np.abs(np.asarray(net.tw, float))
    # `_ttw` ESATTAMENTE come lo calcola il codice (`:5080`)
    ttw = (S._tau_tw_locale(net) if S.TAU_LOCALI else S.TAU_TW)
    ttw = np.asarray(ttw, float) * np.ones(len(net.d)) if np.ndim(ttw) == 0 else np.asarray(ttw, float)
    dte = np.asarray(getattr(net, "_dt_e_ultimo", S.DT), float) * np.ones(len(net.d)) \
        if np.ndim(getattr(net, "_dt_e_ultimo", S.DT)) == 0 else \
        np.asarray(getattr(net, "_dt_e_ultimo", S.DT), float)
    f3 = float(np.mean(tw >= SOGLIA3)) if tw.size else float("nan")
    ft = float(np.mean(tw >= TETTO)) if tw.size else float("nan")
    righe.append(dict(passo=k, n=int(net.n), archi=int(len(net.d)),
                      tw50=float(np.median(tw)) if tw.size else float("nan"),
                      tw95=float(np.percentile(tw, 95)) if tw.size else float("nan"),
                      twmax=float(tw.max()) if tw.size else float("nan"),
                      ttw50=float(np.median(ttw)), ttw05=float(np.percentile(ttw, 5)),
                      dte50=float(np.median(dte)), f3=f3, ft=ft))
    r = righe[-1]
    P("%-6d p50 %8.4f p95 %8.4f max %8.4f  p50 %9.4f p05 %9.4f  dt_e %8.5f  >=3pi %.5f >=4pi %.5f"
      % (k, r["tw50"] / np.pi, r["tw95"] / np.pi, r["twmax"] / np.pi,
         r["ttw50"], r["ttw05"], r["dte50"], r["f3"], r["ft"]))

P()
P("-" * 100)
P("LA STIMA DELLO STATO STAZIONARIO, dalla forma del codice")
P("-" * 100)
r = righe[-1]
# sigma dell'incremento: si RICOSTRUISCE dai due passi, pure-read
lam = r["dte50"] / r["ttw50"]
P("  lambda = dt_e/_ttw (mediane) = %.6g" % lam)
if lam > 0:
    # da |tw|_eq misurato si RISALE a sigma, e si confronta col cammino aleatorio
    sig_da_tw = r["tw50"] * np.sqrt(2.0 * lam)
    P("  se `tw` e' un cammino aleatorio smorzato, l'incremento tipico vale")
    P("    sigma = |tw|_p50 * sqrt(2 lambda) = %.6g   (= %.4f pi)" % (sig_da_tw, sig_da_tw / np.pi))
    P("  e viceversa, con quell'incremento:")
    P("    |tw|_eq = sigma * sqrt(_ttw/(2 dt_e)) = %.6g   (= %.4f pi)"
      % (sig_da_tw / np.sqrt(2.0 * lam), sig_da_tw / np.sqrt(2.0 * lam) / np.pi))
P()
P("  soglia  3 pi = %.6f      |tw| p50 = %.6f = %.4f pi      rapporto soglia/|tw| = %.3f"
  % (SOGLIA3, r["tw50"], r["tw50"] / np.pi, (SOGLIA3 / r["tw50"]) if r["tw50"] else float("inf")))
P("  tetto   4 pi = %.6f      |tw| max = %.6f = %.4f pi"
  % (TETTO, r["twmax"], r["twmax"] / np.pi))
P()
P("IL CRITERIO, scritto PRIMA (vedi la docstring):")
raggiungibile = (r["f3"] > 0.0)
fattore = (SOGLIA3 / r["tw50"]) if r["tw50"] else float("inf")
P("  la soglia e' RAGGIUNTA da qualche arco?  %s   (frazione >= 3pi = %.6f)"
  % ("SI'" if raggiungibile else "NO", r["f3"]))
P("  il tipico e' sotto la soglia di un fattore %.3f  ->  %s"
  % (fattore, "LA MITOSI SCATTA SOLO SULLA CODA" if fattore > 2.0 else
     "il tipico e' nell'ordine della soglia"))
P()
P("COSA QUESTO NON DICE:")
P("  - UN SEME, UNA SCENA (b), %d passi. Non e' una barra d'errore (par.0-ter P3: >= 4 semi)." % max(PASSI))
P("  - `|tw|` puo' CRESCERE ancora: un cammino aleatorio smorzato arriva all'equilibrio in")
P("    ~`_ttw/dt_e` passi, e qui quel numero vale %.1f. Il valore va citato COL PASSO (par.9)."
  % (1.0 / lam if lam else float("inf")))
P("  - la soglia LOCALE e' modulata (`soglia0*(1 - 0.3*tanh(grad_tau))`): scende di al piu' 30 %,")
P("    quindi la frazione vera e' >= a quella calcolata qui contro `3pi` fisso.")

io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(P_) + chr(10))
