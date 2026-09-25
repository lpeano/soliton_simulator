# -*- coding: utf-8 -*-
"""**MISURE 1 e 2: `A13` ALLA NASCITA, e LA TRAIETTORIA DEI FIGLI** *(mandato di Luca, 2026-09-25)*.

> `1.` *«`A13` vieta ogni DISTANZA fra nodi sotto `LAM`, connessi o no. La mitosi controlla solo i
> genitori, e nel vuoto SATURO non c'è posto per un nodo a `>= LAM` da tutti. Per ogni figlio di
> mitosi E di Schwinger: distanza dal nodo più vicino fra TUTTI (`cKDTree` sulle posizioni), in
> unità di `LAM`. Quanti nascono sotto `LAM`?»*
>
> `2.` *«Per ogni nato: grado, `rho`, `|omega|` nel tempo. Restano a grado `2`? Verifica dall'AST
> che gli archi nascano SOLO in semina, mitosi e Schwinger. `omega` rientra o resta alto?»*

**✅ LA VERIFICA DALL'AST È GIÀ FATTA, e il risultato è netto:** `self.i` e `self.j` sono scritti
in **QUATTRO punti soli** — `__init__` *(vuoto)*, **`_allaccia`** *(chiamato da `semina`)*, e
**`mitosi`** in **due** siti *(la divisione `:6041-6042` e lo Schwinger `:6163-6164`)*.
**NESSUNA crescita successiva delle relazioni.** Quindi **un figlio nato con grado `2` resta a
grado `2`**, a meno che non nasca un arco che lo tocchi — e questo può succedere **solo** se una
`semina` in volo o una mitosi su un suo arco lo coinvolgono.

**LA MISURA `A13` SI PRENDE AL MOMENTO GIUSTO:** subito **dopo `mitosi()`** e **prima di
`rilassa_disegno()`**, cioè **alle posizioni di NASCITA**. Se la si prendesse a fine passo, il
rilassamento del disegno avrebbe già mosso tutto e la domanda *«nasce dove c'è posto?»* non
avrebbe più un oggetto.

**⚠ E IL CONFRONTO È COL VUOTO SATURO:** la semina `RSA` garantisce `>= LAM` **fra i nodi del
vuoto**; la domanda è se un figlio, nato **al punto medio di un arco**, rispetti la stessa cosa.
**Il nullo è noto: se l'arco vale `d`, il figlio nasce a `d/2` dai genitori**, quindi
`d/2 >= LAM` richiede `d >= 2 LAM` — e la frazione di archi sotto `2 LAM` è **misurata,
`0.2998`**. **Ma la domanda di Luca è più larga: la distanza dal più vicino fra TUTTI.**

**Sola lettura. Nessuna cura.**
"""
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
FUORI = os.path.join(_QUI, "_figli_della_mitosi")
DEST = os.path.join(FUORI, "FIGLI_DELLA_MITOSI.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEMI = [11, 12]
SEP = 4.0
PASSI = 300
ISTANTI = (1, 5, 20, 60, 120, 200, 300)

FIGLIO = r'''
import io, json, os, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import importlib.util as _iu
import _passo
_sp = _iu.spec_from_file_location("sim_fm", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = True
S.SEMINA_MATURA = True
S.SCALA_MIN_PASSO = True
S.SCALA_MIN = False
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
LAM = float(S.LAM)
n0 = int(net.n)

# ---- MISURA 1: l'involucro su `mitosi`, che guarda ALLE POSIZIONI DI NASCITA ----------------
NASCITE = []
_orig_mit = S.Rete.mitosi


def _wrap_mit(self):
    _n_pre = int(self.n)
    _mit_pre = int(getattr(self, "_g_nati_mitosi", 0))
    _sch_pre = int(getattr(self, "_g_nati_schwinger", 0))
    _fuori = _orig_mit(self)
    _n_post = int(self.n)
    if _n_post > _n_pre:
        _pos = np.asarray(self.pos, float)
        _nuovi = np.arange(_n_pre, _n_post)
        # LA DISTANZA DAL PIU' VICINO FRA TUTTI: `k=2` perche' il primo vicino e' se stesso
        _T = cKDTree(_pos)
        _dd = _T.query(_pos[_nuovi], k=2)[0][:, 1]
        _d_mit = int(getattr(self, "_g_nati_mitosi", 0)) - _mit_pre
        _d_sch = int(getattr(self, "_g_nati_schwinger", 0)) - _sch_pre
        # il canale si distingue dai CONTATORI, non dall'ordine: i figli della divisione
        # vengono prima, gli antinodi Schwinger dopo. E se i conti non tornano, SI DICHIARA.
        _canale = (["mitosi"] * min(_d_mit, len(_nuovi))
                   + ["schwinger"] * max(0, len(_nuovi) - _d_mit))
        _quadra = bool(_d_mit + _d_sch == len(_nuovi))
        # il grado ALLA NASCITA
        _g = np.zeros(_n_post, int)
        _ii = np.asarray(self.i, int); _jj = np.asarray(self.j, int)
        _m = (_ii < _n_post) & (_jj < _n_post)
        np.add.at(_g, _ii[_m], 1); np.add.at(_g, _jj[_m], 1)
        for _k, _idx in enumerate(_nuovi):
            NASCITE.append(dict(nodo=int(_idx), passo=int(PASSO[0]),
                                dist_min=float(_dd[_k]), dist_su_LAM=float(_dd[_k] / LAM),
                                canale=(_canale[_k] if _k < len(_canale) else "?"),
                                grado_nascita=int(_g[_idx]), quadra=_quadra,
                                d_mit=_d_mit, d_sch=_d_sch, nuovi=int(len(_nuovi))))
    return _fuori


S.Rete.mitosi = _wrap_mit
PASSO = [0]

# ---- MISURA 2: la traiettoria dei nati -----------------------------------------------------
TRAI = []


def _istantanea(net, passo):
    n = int(net.n)
    om = np.linalg.norm(np.asarray(net.omega_s, float), axis=1) if np.size(net.omega_s) \
        else np.zeros(n)
    om = om[:n] if om.size >= n else np.pad(om, (0, n - om.size))
    rho = np.asarray(net._rho_sorgente(), float)
    rho = rho[:n] if rho.size >= n else np.pad(rho, (0, n - rho.size))
    g = np.zeros(n, int)
    ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
    m = (ii < n) & (jj < n)
    np.add.at(g, ii[m], 1); np.add.at(g, jj[m], 1)
    nati = np.arange(n0, n)
    o = dict(passo=int(passo), n=n, nati=int(nati.size))
    for et, sel in (("nati", nati), ("orig", np.arange(min(n0, n)))):
        if not sel.size:
            continue
        o["grado_%s_p50" % et] = float(np.median(g[sel]))
        o["grado_%s_max" % et] = float(g[sel].max())
        o["grado_%s_fraz2" % et] = float(np.mean(g[sel] == 2))
        o["rho_%s_p50" % et] = float(np.median(rho[sel]))
        o["om_%s_p50" % et] = float(np.median(om[sel]))
        o["om_%s_max" % et] = float(om[sel].max())
    o["al_pavimento_cum"] = int(getattr(net, "_inerzia_al_pavimento", 0))
    o["inerzia_tot_cum"] = int(getattr(net, "_inerzia_tot", 0))
    return o


TRAI.append(_istantanea(net, 0))
for k in range(1, PASSI + 1):
    PASSO[0] = k
    _passo.passo_pieno(S, net)
    if k in ISTANTI:
        TRAI.append(_istantanea(net, k))

out = dict(SEME=SEME, LAM=LAM, n0=n0, n_fin=int(net.n), PASSI=int(PASSI),
           nascite=NASCITE, traiettoria=TRAI,
           frazione_archi_sotto_2lam_ini=None)
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(out))
print("OK %s  n %d -> %d  nascite registrate %d" % (NOME, n0, net.n, len(NASCITE)))
'''


def braccio(seme):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nPASSI = %d\nISTANTI = %r\n"
           % (RADICE, TMP, "s%d" % seme, seme, SEP, PASSI, list(ISTANTI))) + FIGLIO
    p = os.path.join(TMP, "_br_s%d.py" % seme)
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


RILEGGI = ("--rileggi" in sys.argv)
LOG = []
if RILEGGI:
    for s in SEMI:
        if not os.path.isfile(os.path.join(TMP, "s%d.json" % s)):
            raise SystemExit("[rileggi] manca s%d.json: non rileggo a meta'." % s)
        LOG.append("[s%d] RILETTO dal json" % s)
else:
    proc = {s: braccio(s) for s in SEMI}
    for s, pr in proc.items():
        so, se = pr.communicate()
        LOG.append("[s%d] rc=%d %s" % (s, pr.returncode,
                                       (so or b"").decode("utf-8", "replace").strip()[-140:]))
        if pr.returncode:
            LOG.append((se or b"").decode("utf-8", "replace")[-1600:])

P_ = []


def P(x=""):
    P_.append(x)


P("=" * 120)
P("MISURE 1 e 2 — `A13` ALLA NASCITA, e LA TRAIETTORIA DEI FIGLI. **Sola lettura.**")
P("=" * 120)
P()
P("  " + _passo.descrivi())
P("  scena (ii) (b), campo MATURO, freno ON, %d passi, %d semi, un processo per braccio."
  % (PASSI, len(SEMI)))
P()
P("✅ LA VERIFICA DALL'AST (misura 2, la parte che non richiede un run):")
P("   `self.i` e `self.j` sono scritti in QUATTRO punti SOLI:")
P("     `:1624`  __init__     (il vuoto)")
P("     `:2851`  _allaccia    (chiamato da `semina`)")
P("     `:6041`  mitosi       la DIVISIONE")
P("     `:6163`  mitosi       lo SCHWINGER")
P("   **NESSUNA crescita successiva delle relazioni.** Un figlio nato con grado 2 resta a")
P("   grado 2, se non lo tocca un arco nuovo -- e un arco nuovo puo' venire solo da quei siti.")
P()
for l in LOG:
    P(l)
P()
if any("rc=1" in l for l in LOG):
    P("STOP: un braccio non e' arrivato in fondo.")
    io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(P_) + chr(10))
    print(chr(10).join(P_))
    sys.exit(1)

D = {}
for s in SEMI:
    D[s] = json.loads(io.open(os.path.join(TMP, "s%d.json" % s), encoding="utf-8").read())

# ---------------------------------------------------------------- MISURA 1
P("-" * 120)
P("1. `A13` ALLA NASCITA — distanza dal nodo PIU' VICINO fra TUTTI, alle posizioni di NASCITA")
P("-" * 120)
LAM = D[SEMI[0]]["LAM"]
P("  LAM = %.6f. La misura e' presa SUBITO DOPO `mitosi()` e PRIMA di `rilassa_disegno()`." % LAM)
P()
tot = {"mitosi": [], "schwinger": [], "?": []}
quadra_ko = 0
for s in SEMI:
    for x in D[s]["nascite"]:
        tot.setdefault(x["canale"], []).append(x)
        if not x.get("quadra", True):
            quadra_ko += 1
P("  %-12s %-8s %-12s %-12s %-12s %-14s %-14s"
  % ("canale", "nati", "d/LAM p05", "d/LAM p50", "d/LAM min", "sotto LAM", "sotto 0.5 LAM"))
for can in ("mitosi", "schwinger", "?"):
    v = tot.get(can) or []
    if not v:
        P("  %-12s %-8d  (nessuno)" % (can, 0))
        continue
    a = np.asarray([x["dist_su_LAM"] for x in v], float)
    P("  %-12s %-8d %-12.4f %-12.4f %-12.4f %-14.6f %-14.6f"
      % (can, a.size, np.percentile(a, 5), np.median(a), a.min(),
         float(np.mean(a < 1.0)), float(np.mean(a < 0.5))))
P()
if quadra_ko:
    P("  ⚠ in %d eventi i contatori NON quadravano con il numero di nodi nuovi: l'attribuzione" % quadra_ko)
    P("    del canale li' e' INCERTA, e lo dico invece di nasconderlo.")
tutte = np.asarray([x["dist_su_LAM"] for s in SEMI for x in D[s]["nascite"]], float)
if tutte.size:
    P("  TUTTI I NATI (%d): sotto LAM = %.6f      sotto 0.5 LAM = %.6f      min = %.6f LAM"
      % (tutte.size, float(np.mean(tutte < 1.0)), float(np.mean(tutte < 0.5)), tutte.min()))
    P()
    if np.mean(tutte < 1.0) > 0:
        P("  -> ⛔ **`A13` È VIOLATO ALLA NASCITA, e in silenzio:** il %.2f %% dei nati nasce a meno"
          % (100.0 * np.mean(tutte < 1.0)))
        P("     di `LAM` dal suo vicino piu' prossimo. La mitosi controlla SOLO i genitori.")
    else:
        P("  -> `A13` NON e' violato alla nascita: tutti i nati stanno a `>= LAM` da TUTTI.")
P()
P("  ➕ LA CURA SENZA LEGGI NUOVE, VALUTATA E **NON SCRITTA** (`STANDARD 10`):")
P("     **`A13` applicato alla nascita**: un nodo nasce **solo dove c'e' posto**.")
P("     Non e' una legge nuova: e' `A13` che vale gia' per la semina, esteso al sito che non")
P("     lo applica. **Quanti eventi di oggi sopravvivrebbero?**")
if tutte.size:
    P("       eventi di nascita registrati: %d" % tutte.size)
    P("       che sopravvivono (`d >= LAM` da TUTTI): %d  = %.4f"
      % (int(np.sum(tutte >= 1.0)), float(np.mean(tutte >= 1.0))))
    P("     ⚠ E IL COSTO VA DETTO: se la frazione che sopravvive e' piccola, applicare `A13`")
    P("       alla nascita **non regola la mitosi: la SPEGNE**. Il numero qui sopra dice quale")
    P("       dei due casi sia, e NON e' una decisione mia.")
P()

# ---------------------------------------------------------------- MISURA 2
P("-" * 120)
P("2. LA TRAIETTORIA DEI FIGLI — grado, `rho`, `|omega|` nel tempo. NATI contro ORIGINALI")
P("-" * 120)


def md(campo, k):
    v = [next((x[campo] for x in D[s]["traiettoria"] if x["passo"] == k and campo in x), None)
         for s in SEMI]
    v = [y for y in v if y is not None]
    return float(np.mean(v)) if v else float("nan")


P("  %-6s %-7s %-24s %-24s %-24s %-22s"
  % ("passo", "nati", "grado (nati/orig)", "frazione a grado 2", "rho (nati/orig)",
     "|omega| p50 (nati/orig)"))
for k in (0,) + ISTANTI:
    if md("n", k) != md("n", k):
        continue
    P("  %-6d %-7.0f %-24s %-24s %-24s %-22s"
      % (k, md("nati", k),
         "%.1f / %.1f" % (md("grado_nati_p50", k), md("grado_orig_p50", k)),
         "%.4f / %.4f" % (md("grado_nati_fraz2", k), md("grado_orig_fraz2", k)),
         "%.4g / %.4g" % (md("rho_nati_p50", k), md("rho_orig_p50", k)),
         "%.4g / %.4g" % (md("om_nati_p50", k), md("om_orig_p50", k))))
P()
P("  |omega| MASSIMO fra i nati contro fra gli originali:")
for k in ISTANTI:
    a, b = md("om_nati_max", k), md("om_orig_max", k)
    if a != a:
        continue
    P("    passo %-6d nati %-14.6g   originali %-14.6g   rapporto %.4g"
      % (k, a, b, a / b if b else float("inf")))
P()
kf = max(ISTANTI)
f2 = md("grado_nati_fraz2", kf)
P("  -> RESTANO A GRADO 2? frazione dei nati con grado esattamente 2 al passo %d: **%.4f**"
  % (kf, f2))
if f2 > 0.9:
    P("     ** SÌ: %.1f %% dei nati resta a grado 2. Coerente con l'AST: nessuna crescita" % (100 * f2))
    P("        successiva delle relazioni. **")
elif f2 < 0.1:
    P("     ** NO: quasi nessuno resta a grado 2 -- qualcosa li allaccia. Va spiegato. **")
else:
    P("     ** IN PARTE: %.1f %%. Alcuni vengono toccati da archi nuovi, altri no. **" % (100 * f2))
P()
o1, o2 = md("om_nati_p50", ISTANTI[0]), md("om_nati_p50", kf)
P("  -> `omega` RIENTRA O RESTA ALTO? mediana dei nati: %.6g al passo %d  ->  %.6g al passo %d"
  % (o1, ISTANTI[0], o2, kf))
P("     e la mediana degli ORIGINALI: %.6g -> %.6g"
  % (md("om_orig_p50", ISTANTI[0]), md("om_orig_p50", kf)))
if o1 and o2 / o1 < 0.5:
    P("     ** RIENTRA: cala di un fattore %.3g. **" % (o1 / o2 if o2 else float("inf")))
elif o1 and o2 / o1 > 2.0:
    P("     ** RESTA ALTO E SALE: x%.3g. **" % (o2 / o1))
else:
    P("     ** RESTA sullo stesso ordine (x%.3g). **" % (o2 / o1 if o1 else float("nan")))
P()
P("  E IL PAVIMENTO DELL'INERZIA, dai contatori GIA' cablati nel simulatore:")
for k in ISTANTI:
    a, b = md("al_pavimento_cum", k), md("inerzia_tot_cum", k)
    if a != a or not b:
        continue
    P("    passo %-6d al pavimento %-14.0f su %-14.0f  =  %.6f" % (k, a, b, a / b))
P("    (`_inerzia_al_pavimento` / `_inerzia_tot`: cumulativi, e la legge oggi e'")
P("     `inerzia = max(_contrasto * _T2, 1e-6)`, NON `max(_rho_sorgente(), 1e-6)`.")
P("     ⚠ IL CANDIDATO CHE AVEVO CITATO USAVA LA FORMA SUPERATA: il commento a `:3226` dice")
P("     'Era: inerzia = max(rho_sorgente * (CS_M/cs)^2, 1e-6)'. La forma e' cambiata.)")
P()
P("COSA QUESTO NON DICE:")
P("  - DUE SEMI: par.0-ter `P3` chiede >= 4 per una barra fra semi.")
P("  - l'attribuzione del CANALE (mitosi o Schwinger) viene dai contatori, non dall'ordine, e")
P("    quando i conti non quadrano il referto lo DICE invece di scegliere.")
P("  - `A13` e' misurato SULLE POSIZIONI (`pos`): e' l'unica cosa che oggi esiste, ed è anche")
P("    il motivo per cui `A3` (il disegno che esce dalla dinamica) tocca questa misura.")
P("  - SOLA LETTURA. Nessuna cura.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
