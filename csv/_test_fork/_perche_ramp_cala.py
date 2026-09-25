# -*- coding: utf-8 -*-
"""**PERCHE' LA RAMPA CALA DOPO IL PASSO 1**, nella configurazione della CAMPAGNA.

> Il sigillo di `CURA 4`, rifatto **dal CLI** (`CLI-1`), da' `A2 = FAIL`: al passo 1
> `ramp == 1` su **54 nodi su 4252** invece che su tutti, e `_g_rampa_cali = 4198`.
> **Al passo ZERO invece `ramp = 1.000000000000000` su TUTTI** (`min = max = 1`).
> **Quindi la cura FA cio' che dichiara alla nascita, e poi la rampa SCENDE.**

`ramp = min(1, eta / _tempo_rampa())`, e con la cura accesa il denominatore e' il
**TEMPO-LUCE** `_tempo_luce_nodo(i, j)`, non `TAU_A`. **Sono DUE quantita' che si muovono
entrambe**: `eta` cresce di `dt_n` per passo, il tempo-luce cambia con `d` e con `cs`.
**Se il denominatore cresce piu' del numeratore, un nodo MATURO torna IMMATURO.**

**COSA MISURA, senza toccare nessun flag** *(la configurazione e' quella del driver,
catturata da `_cli_flag`)*: fra il passo 0 e il passo 1, **di quanto cambiano
SEPARATAMENTE** `eta` e `_tempo_rampa`, e quale dei due muove il rapporto.
**Il nullo e' dichiarato: se la rampa calasse per `eta` FERMA, il rapporto `eta1/eta0`
sarebbe 1; se calasse per il denominatore, sarebbe `tr1/tr0 > eta1/eta0`.**

ASCII puro. Sola lettura: nessuna riga del simulatore cambia.
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _cli_flag
import _presidio

_presidio.avvia(__file__)

import numpy as np

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_perche_ramp_cala", "REFERTO.txt")
os.makedirs(os.path.dirname(DEST), exist_ok=True)
SEME = 11
SEP = 4.0

R = []


def P(s=""):
    R.append(s)


# l'argv VERA del driver, piu' `--nodi 0` (il vuoto di `_applica_flag` non si usa: la scena
# la costruisce questa sonda, esattamente come fa il sigillo)
_S0, ARGV = _cli_flag.argv_del_driver([], dest=os.path.join(_QUI, "_perche_ramp_cala", "_sc"))
ARGV = ARGV + ["--nodi", "0"]
S, _a = _cli_flag.carica_dal_cli(_cli_flag.argv_per(
    os.path.join(RADICE, "soliton_simulator.py"), ARGV)[0], nome="sim_ramp")

S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = SEP
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
n0 = int(net.n)


def stato():
    tr = net._tempo_rampa()
    tr = np.asarray(tr, float) if np.ndim(tr) else np.full(net.n, float(tr))
    eta = np.asarray(net.eta, float)
    return eta.copy(), tr.copy(), np.minimum(1.0, eta / tr)


e0, t0, r0 = stato()
net.step()
e1, t1, r1 = stato()
k = np.arange(n0)                      # solo i nodi della semina iniziale

P("=" * 100)
P("PERCHE' LA RAMPA CALA -- configurazione della CAMPAGNA (argv del driver), seme %d" % SEME)
P("=" * 100)
P()
P("SEMINA_MATURA %s   CS_DINAMICO %s   TAU_LUCE %s   nodi iniziali %d"
  % (S.SEMINA_MATURA, S.CS_DINAMICO, S.TAU_LUCE, n0))
P()
P("%-22s %-18s %-18s %-18s" % ("grandezza", "passo 0 (p50)", "passo 1 (p50)", "rapporto 1/0"))
for nome, a, b in (("eta (numeratore)", e0[k], e1[k]),
                   ("_tempo_rampa (den.)", t0[k], t1[k]),
                   ("ramp = min(1, e/t)", r0[k], r1[k])):
    m0, m1 = float(np.median(a)), float(np.median(b))
    P("%-22s %-18.9f %-18.9f %-18.6f" % (nome, m0, m1, (m1 / m0) if m0 else float("nan")))
P()
P("ramp al passo 0:  min %.15f   max %.15f   uguali a 1: %d su %d"
  % (r0[k].min(), r0[k].max(), int(np.sum(r0[k] == 1.0)), n0))
P("ramp al passo 1:  min %.15f   max %.15f   uguali a 1: %d su %d"
  % (r1[k].min(), r1[k].max(), int(np.sum(r1[k] == 1.0)), n0))
P()
_su_eta = float(np.median(e1[k] / e0[k]))
_su_tr = float(np.median(t1[k] / t0[k]))
P("CRESCITA MEDIANA SEPARATA:   eta x%.6f     _tempo_rampa x%.6f" % (_su_eta, _su_tr))
P()
if _su_tr > _su_eta:
    P("-> IL DENOMINATORE CRESCE PIU' DEL NUMERATORE: e' IL TEMPO-LUCE che sale, non `eta`")
    P("   che si ferma. **Un nodo MATURO torna IMMATURO perche' la sua scala di")
    P("   riferimento si e' allungata.**")
else:
    P("-> NON e' il denominatore: `eta` cresce meno di quanto il tempo-luce cambi. Il calo")
    P("   viene dal NUMERATORE, e la diagnosi qui sopra NON regge.")
P()
P("E DI CHE COSA E' FATTO IL DENOMINATORE (`d_nodo / cs_nodo`):")
try:
    _cs = np.asarray(getattr(net, "_cs_nodo_prev", np.full(net.n, S.CS_M)), float)
    P("  cs per nodo al passo 1:  p05 %.6f  p50 %.6f  p95 %.6f   CS_M %.6f   cs_std/cs %.4f %%"
      % (np.percentile(_cs, 5), np.median(_cs), np.percentile(_cs, 95), S.CS_M,
         100.0 * float(np.std(_cs) / np.mean(_cs))))
except Exception as _e:
    P("  cs per nodo: non leggibile (%s)" % _e)
P()
P("COSA QUESTA SONDA *NON* DICE:")
P("  - NON dice se il calo sia un difetto o la legge: dice DA DOVE viene. La decisione e' di Luca.")
P("  - un seme, una scena, DUE passi. Il calo a tempi lunghi non e' misurato qui.")
P("  - non tocca nessun flag: spegnere `--cs-dinamico` per vedere se il calo sparisce sarebbe")
P("    una misura DIVERSA, e cambierebbe la configurazione invece di leggerla (`P2`).")

T = chr(10).join(R) + chr(10)
io.open(DEST, "w", encoding="utf-8", newline=chr(10)).write(T)
print(T)
