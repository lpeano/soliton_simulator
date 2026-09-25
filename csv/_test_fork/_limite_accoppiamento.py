# -*- coding: utf-8 -*-
"""**MISURA 3: IL LIMITE DI ACCOPPIAMENTO DEBOLE** *(mandato di Luca, 2026-09-25)*.

> *«Su un nodo normale, togli archi fino a `k = 77, 20, 8, 4, 2` (copia della rete, un processo
> per caso) e misura COPPIA e INERZIA separatamente. Se `omega = coppia/inerzia` esplode per `k`
> piccolo, la legge dell'inerzia NON regge il limite: è un difetto della legge, non del nodo, e
> vale qualunque strada si scelga.»*

**COPPIA E INERZIA SONO VARIABILI LOCALI di `_passo_spinoriale`** *(`:3332` e `:3338`)*, quindi
non si leggono da fuori. **Si usa una COPIA del simulatore con DUE assegnazioni diagnostiche**
— `self._diag_inerzia` e `self._diag_coppia` — **e il file vero NON si tocca**, perché il mandato
dice *sola lettura*.

**Il blob di ENTRAMBI i file va nel referto** *(par.5-quinquies: il codice di una misura
dev'essere recuperabile per costruzione)*, e la copia è scritta **accanto ai dati**.

**⚠ UNA CORREZIONE A CIÒ CHE HO CITATO IO:** la legge è
**`inerzia = max(_contrasto * _T2, 1e-6)`** con `_contrasto = rho_s/peq_nodo` e `_T2` il
tempo-luce al quadrato — **NON `max(_rho_sorgente(), 1e-6)`**, che il commento a `:3226` dichiara
**superata**: *«Era: `inerzia = max(rho_sorgente * (CS_M/cs)^2, 1e-6)`»*.

**IL CRITERIO È SCRITTO PRIMA:** *se `|coppia|` resta dello stesso ordine e `inerzia` CROLLA al
calare di `k`, allora `omega` esplode **per la legge dell'inerzia**, non per il nodo.*
**E il caso opposto è altrettanto informativo:** se `inerzia` regge e **la coppia** cresce, il
difetto è nella coppia.

**Sola lettura sul simulatore. Nessuna cura.**
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _passo
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
FUORI = os.path.join(_QUI, "_limite_accoppiamento")
DEST = os.path.join(FUORI, "LIMITE_ACCOPPIAMENTO.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEMI = [11, 12]
SEP = 4.0
GRADI = [77, 20, 8, 4, 2]
PASSI_PRIMA = 20      # quanti passi PIENI prima di operare: il campo deve esistere

# ------------------------------------------------- LA COPIA con due assegnazioni diagnostiche
SIM = os.path.join(RADICE, "soliton_simulator.py")
COPIA = os.path.join(FUORI, "_sim_diag.py")
src = io.open(SIM, encoding="utf-8", newline="").read()
blob_vero = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()[:8]

A = "        inerzia = np.maximum(_contrasto * _T2, 1e-6)       # il pavimento RESTA"
assert src.count(A) == 1, "l'ancora dell'inerzia non e' unica: %d" % src.count(A)
src2 = src.replace(A, "        inerzia = np.maximum(_contrasto * _T2, 1e-6)\n"
                      "        self._diag_inerzia = np.array(inerzia, copy=True)  # DIAGNOSTICO\n"
                      "        self._diag_contrasto = np.array(_contrasto, copy=True)\n"
                      "        self._diag_T2 = np.array(_T2, copy=True)\n"
                      "        _ = 1  # il pavimento RESTA", 1)
B = "        omega_new = omega_src + dtn_c * (correzione / inerzia[:, None] - omega_src / _tau)"
assert src2.count(B) == 1, "l'ancora di omega_new non e' unica"
src2 = src2.replace(B, "        self._diag_coppia = np.array(correzione, copy=True)  # DIAGNOSTICO\n"
                    + B, 1)
io.open(COPIA, "w", encoding="utf-8", newline="\n").write(src2)
blob_copia = hashlib.sha1(io.open(COPIA, "rb").read()).hexdigest()[:8]

FIGLIO = r'''
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import importlib.util as _iu
import _passo
_sp = _iu.spec_from_file_location("sim_la", COPIA)
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
# il campo deve ESISTERE: `PASSI_PRIMA` passi PIENI prima di operare
for _ in range(PASSI_PRIMA):
    _passo.passo_pieno(S, net)

n = int(net.n)
ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
grado = np.zeros(n, int)
m = (ii < n) & (jj < n)
np.add.at(grado, ii[m], 1); np.add.at(grado, jj[m], 1)
# IL NODO BERSAGLIO: uno NORMALE, cioe' col grado piu' vicino alla MEDIANA. Non il massimo,
# non il minimo: la domanda e' sul limite, e il punto di partenza deve essere tipico.
gm = int(np.median(grado))
cand = np.where(grado == gm)[0]
if not cand.size:
    cand = np.array([int(np.argmin(np.abs(grado - gm)))])
BERS = int(cand[0])

# IL TAGLIO: si TOLGONO archi del bersaglio fino a `K`. Si tolgono gli archi PIU' LUNGHI per
#   primi -- una scelta, e la dichiaro: togliere i piu' CORTI cambierebbe il vicinato piu'
#   vicino, che e' quello che pesa di piu' nel kernel `exp(-d/lam)`. Togliere i piu' lunghi
#   e' il taglio MENO invasivo a parita' di `k`.
d = np.asarray(net.d, float)
suoi = np.where((ii == BERS) | (jj == BERS))[0]
ordine_tagli = suoi[np.argsort(d[suoi])[::-1]]     # dal piu' LUNGO al piu' corto

o = dict(SEME=SEME, n=n, bersaglio=BERS, grado_iniziale=int(grado[BERS]),
         grado_mediano=gm, archi_suoi=int(suoi.size), casi=[])

for K in GRADI:
    if K > suoi.size:
        o["casi"].append(dict(K=int(K), salta="il bersaglio ha solo %d archi" % suoi.size))
        continue
    # UNA COPIA DELLA RETE per caso: si ricostruisce da zero e si rifa' il taglio, cosi' i
    # casi sono INDIPENDENTI (non si tagliano a cascata sullo stesso oggetto).
    import copy as _copy
    net2 = _copy.deepcopy(net)
    quanti = int(suoi.size - K)
    via = set(int(x) for x in ordine_tagli[:quanti])
    keep = np.array([k not in via for k in range(len(net2.d))], bool)
    for _nome in ("i", "j", "d", "d0", "vd", "tw", "twp", "eta_arco"):
        _v = getattr(net2, _nome, None)
        if isinstance(_v, np.ndarray) and _v.shape[0] == keep.size:
            setattr(net2, _nome, _v[keep])
    for _nome in list(vars(net2)):
        _v = getattr(net2, _nome)
        if isinstance(_v, np.ndarray) and _v.ndim >= 1 and _v.shape[0] == keep.size \
                and _nome not in ("i", "j", "d", "d0"):
            setattr(net2, _nome, _v[keep])
    net2._S = None; net2._perm = None; net2._ker_cache = None
    net2._cicli_topologici = None
    # UN passo PIENO, e si leggono i diagnostici
    try:
        _passo.passo_pieno(S, net2)
        _in = np.asarray(getattr(net2, "_diag_inerzia", []), float)
        _co = np.asarray(getattr(net2, "_diag_coppia", []), float)
        _ct = np.asarray(getattr(net2, "_diag_contrasto", []), float)
        _t2 = np.asarray(getattr(net2, "_diag_T2", []), float)
        _om = np.linalg.norm(np.asarray(net2.omega_s, float), axis=1)
        _g = np.zeros(int(net2.n), int)
        _i2 = np.asarray(net2.i, int); _j2 = np.asarray(net2.j, int)
        _m2 = (_i2 < net2.n) & (_j2 < net2.n)
        np.add.at(_g, _i2[_m2], 1); np.add.at(_g, _j2[_m2], 1)
        c = dict(K=int(K), grado_vero=int(_g[BERS]) if BERS < _g.size else -1,
                 archi_tolti=quanti, archi_rimasti=int(keep.sum()))
        if _in.size > BERS:
            c["inerzia"] = float(_in[BERS])
            c["al_pavimento"] = bool(_in[BERS] <= 1e-6)
        if _ct.size > BERS:
            c["contrasto"] = float(_ct[BERS])
        if _t2.size > BERS:
            c["T2"] = float(_t2[BERS])
        if _co.size > BERS:
            c["coppia"] = float(np.linalg.norm(_co[BERS]))
        if _om.size > BERS:
            c["omega"] = float(_om[BERS])
        if "coppia" in c and "inerzia" in c and c["inerzia"]:
            c["coppia_su_inerzia"] = c["coppia"] / c["inerzia"]
        o["casi"].append(c)
    except Exception as e:
        o["casi"].append(dict(K=int(K), errore=str(e)[:160]))

io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  bersaglio %d (grado %d), casi %d" % (NOME, BERS, o["grado_iniziale"],
                                                   len(o["casi"])))
'''


def braccio(seme):
    src_ = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nCOPIA = %r\nGRADI = %r\n"
            "PASSI_PRIMA = %d\n"
            % (RADICE, TMP, "s%d" % seme, seme, SEP, COPIA, GRADI, PASSI_PRIMA)) + FIGLIO
    p = os.path.join(TMP, "_br_s%d.py" % seme)
    io.open(p, "w", encoding="utf-8", newline="\n").write(src_)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


LOG = []
proc = {s: braccio(s) for s in SEMI}
for s, pr in proc.items():
    so, se = pr.communicate()
    LOG.append("[s%d] rc=%d %s" % (s, pr.returncode,
                                   (so or b"").decode("utf-8", "replace").strip()[-140:]))
    if pr.returncode:
        LOG.append((se or b"").decode("utf-8", "replace")[-1800:])

P_ = []


def P(x=""):
    P_.append(x)


P("=" * 120)
P("MISURA 3 — **IL LIMITE DI ACCOPPIAMENTO DEBOLE**. Sola lettura sul simulatore.")
P("=" * 120)
P()
P("  " + _passo.descrivi())
P("  scena (ii) (b), campo MATURO, freno ON, %d passi PIENI prima di operare, %d semi."
  % (PASSI_PRIMA, len(SEMI)))
P()
P("  LA COPIA DEL SIMULATORE, e i due blob (par.5-quinquies):")
P("    file VERO   sha1-byte %s   (NON toccato: il mandato dice sola lettura)" % blob_vero)
P("    COPIA       sha1-byte %s   %s" % (blob_copia, os.path.relpath(COPIA, RADICE)))
P("    la copia aggiunge SOLO assegnazioni diagnostiche: `_diag_inerzia`, `_diag_contrasto`,")
P("    `_diag_T2`, `_diag_coppia`. **Coppia e inerzia sono LOCALI di `_passo_spinoriale`**")
P("    (`:3332`, `:3338`), quindi da fuori non si leggono.")
P()
P("  ⚠ LA LEGGE DELL'INERZIA OGGI, e va detta giusta:")
P("     `inerzia = max(_contrasto * _T2, 1e-6)`  con `_contrasto = rho_s/peq_nodo`")
P("     **NON** `max(_rho_sorgente(), 1e-6)`, che il commento a `:3226` dichiara SUPERATA.")
P("     **Il candidato che avevo citato io usava la forma vecchia.**")
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

P("-" * 120)
P("IL BERSAGLIO: un nodo NORMALE, col grado piu' vicino alla MEDIANA (non il massimo, non il")
P("minimo: la domanda e' sul LIMITE, e il punto di partenza deve essere TIPICO).")
for s in SEMI:
    P("  seme %-4d nodo %-6d grado iniziale %-5d (mediano %d), archi suoi %d"
      % (s, D[s]["bersaglio"], D[s]["grado_iniziale"], D[s]["grado_mediano"],
         D[s]["archi_suoi"]))
P()
P("  IL TAGLIO: si tolgono gli archi PIU' LUNGHI per primi. **E' una scelta, e la dichiaro:**")
P("  togliere i piu' CORTI cambierebbe il vicinato prossimo, che pesa di piu' nel kernel")
P("  `exp(-d/lam)`. Togliere i piu' lunghi e' il taglio MENO invasivo a parita' di `k`.")
P("  E OGNI CASO PARTE DA UNA COPIA FRESCA della rete: i casi sono INDIPENDENTI, non a cascata.")
P()
P("-" * 120)
P("%-6s %-8s %-14s %-14s %-14s %-14s %-14s %-10s"
  % ("k", "grado", "COPPIA", "INERZIA", "coppia/inerzia", "|omega|", "contrasto", "al pav."))
P("-" * 120)


def mc(s, K, campo):
    for c in D[s]["casi"]:
        if c.get("K") == K and campo in c:
            return c[campo]
    return None


for K in GRADI:
    v = {}
    for campo in ("grado_vero", "coppia", "inerzia", "coppia_su_inerzia", "omega", "contrasto"):
        vals = [mc(s, K, campo) for s in SEMI]
        vals = [x for x in vals if x is not None]
        v[campo] = float(np.mean(vals)) if vals else float("nan")
    pav = [mc(s, K, "al_pavimento") for s in SEMI]
    pav = [x for x in pav if x is not None]
    err = [c.get("errore") or c.get("salta") for s in SEMI for c in D[s]["casi"]
           if c.get("K") == K and (c.get("errore") or c.get("salta"))]
    if err:
        P("%-6d  SALTATO / ERRORE: %s" % (K, err[0]))
        continue
    P("%-6d %-8.0f %-14.6g %-14.6g %-14.6g %-14.6g %-14.6g %-10s"
      % (K, v["grado_vero"], v["coppia"], v["inerzia"], v["coppia_su_inerzia"],
         v["omega"], v["contrasto"], ("%d/%d" % (sum(1 for x in pav if x), len(pav)))
         if pav else "?"))
P()
P("=" * 120)
P("IL CRITERIO, scritto PRIMA: se `|coppia|` resta dello stesso ordine e `inerzia` CROLLA al")
P("calare di `k`, `omega` esplode **per la legge dell'inerzia**, non per il nodo.")
P("=" * 120)


def serie(campo):
    out = []
    for K in GRADI:
        vals = [mc(s, K, campo) for s in SEMI]
        vals = [x for x in vals if x is not None]
        out.append(float(np.mean(vals)) if vals else None)
    return out


co = serie("coppia")
ine = serie("inerzia")
ra = serie("coppia_su_inerzia")
val = [k for k, (a, b) in enumerate(zip(co, ine)) if a is not None and b is not None]
if len(val) >= 2:
    k0, k1 = val[0], val[-1]
    fc = co[k1] / co[k0] if co[k0] else float("nan")
    fi = ine[k1] / ine[k0] if ine[k0] else float("nan")
    fr = ra[k1] / ra[k0] if ra[k0] else float("nan")
    P("  da k = %d a k = %d:" % (GRADI[k0], GRADI[k1]))
    P("     COPPIA         x%.4g" % fc)
    P("     INERZIA        x%.4g" % fi)
    P("     coppia/inerzia x%.4g" % fr)
    P()
    if abs(np.log10(abs(fc) + 1e-300)) < 0.5 and fi < 0.1:
        P("  -> ⛔ **LA LEGGE DELL'INERZIA NON REGGE IL LIMITE:** la coppia resta dello stesso")
        P("     ordine (x%.3g) e l'inerzia CROLLA (x%.3g). **E' un difetto della LEGGE, non del" % (fc, fi))
        P("     nodo, e vale qualunque strada si scelga** (rilievo di Luca, criterio scritto prima).")
    elif fc > 10.0:
        P("  -> il difetto e' nella COPPIA, non nell'inerzia: la coppia cresce di x%.3g." % fc)
    elif abs(np.log10(abs(fr) + 1e-300)) < 0.5:
        P("  -> `omega = coppia/inerzia` NON esplode (x%.3g): il limite REGGE." % fr)
    else:
        P("  -> il rapporto cambia di x%.3g, e non per una delle due ragioni pure: entrambe" % fr)
        P("     si muovono. Va letto sui numeri, non sul verdetto.")
else:
    P("  NON MISURATO: meno di due casi validi. Nessun verdetto.")
P()
P("COSA QUESTO NON DICE:")
P("  - DUE SEMI, e UN SOLO nodo bersaglio per seme: e' una PROVA DI LIMITE, non una statistica.")
P("  - il taglio TOGLIE ARCHI A MANO: non e' un processo del sistema, ed e' di proposito --")
P("    la domanda e' se la LEGGE regga un `k` piccolo, non se il sistema ci arrivi da solo.")
P("  - togliere archi cambia anche i VICINI del bersaglio: l'effetto misurato non e' solo suo.")
P("  - SOLA LETTURA sul simulatore: la copia diagnostica NON e' il file che gira nelle campagne,")
P("    e i due blob sono qui sopra.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
