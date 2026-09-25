# -*- coding: utf-8 -*-
r"""**LA SCOMPOSIZIONE ESATTA DEL DIVARIO DEI FIGLI** *(mandato di Luca, 2026-09-26)*.

I criteri stanno in `doc/TASK_HISTORY/2026-09-26_potenze1-scomposizione-figli.md`, **committato
PRIMA di questa raccolta**.

```
log(c_f/c_m) = log[(rho/W^2)_f/(rho/W^2)_m]  +  2 log(W_f/W_m)  -  log(peq_f/peq_m)
                \_________ T1 _________/        \____ T2 ____/     \____ T3 ____/
   T2 = quello che `rho_s/W^2` TOGLIE      T3 = quello che resta a `peq` EREDITATO
```

**COSA SI RACCOGLIE, e le due definizioni che contano:**
* **`W` e' la STESSA `_wn` della cura** — `bincount(i, w) + bincount(j, w)` — **non ricalcolata a
  parte**: una `W` diversa descriverebbe **un'altra cura**;
* **la COPPIA e' la STESSA `correzione`** che entra in `omega_new`, in modulo: ricostruirla da fuori
  e' l'errore gia' fatto in questo repo, che dava **meta' coppia**.

**LE RIGHE DIAGNOSTICHE PASSANO DALLA POSTCONDIZIONE (`P9`):** la copia si genera al run dal file
corrente e **deve differire SOLO** per le righe `self._diag_*` dichiarate — altrimenti **STOP**.

**RIPRENDIBILE:** il json di ogni braccio si scrive **appena quel braccio finisce**, col **blob** del
simulatore e della copia; un json di **blob diverso NON si riusa** (`P5`/`P9`).

**SOLA LETTURA. NESSUNA CURA.** Flag **SPENTO**, `passo_pieno`, 2 semi, budget 120 passi, la stessa
scena del sigillo esteso.

ASCII puro.
"""
import ast
import datetime
import hashlib
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
FUORI = os.path.join(_QUI, "_scomposizione_figli")
DEST = os.path.join(FUORI, "SCOMPOSIZIONE_figli.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)
NL = chr(10)

SEMI = [11, 12]
SEP = 4.0
PASSI_PRIMA = 20
BUDGET = 120
ETA_MAX = 14

SIM = os.path.join(RADICE, "soliton_simulator.py")
blob_vero = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()[:8]

# ============================================================== LA COPIA, con la POSTCONDIZIONE
DIAG_IN = [
    "        self._diag_inerzia = np.array(inerzia, copy=True)",
    "        self._diag_contrasto = np.array(_contrasto, copy=True)",
    "        self._diag_peq_nodo = np.array(_peq_nodo, copy=True)",
    "        self._diag_rho_s = np.array(_rho_s, copy=True)",
    # ⚠ **`_ok_n` E' INDISPENSABILE, e il filtro «tutte positive» NON lo sostituisce:**
    #   dove `_ok_n` e' falso `_contrasto` vale **`1` per CONVENZIONE**, e **`1` e'
    #   POSITIVO**. Quei nodi passerebbero il filtro e **l'identita' non chiuderebbe**.
    #   *(Rilievo di Luca. Nel primo giro erano stati scartati **per caso**, perche' al
    #   primo passo di vita `rho` vale `0.0` ESATTO — non per il filtro: **se `rho` fosse
    #   stato piccolo-ma-non-nullo, `K1` avrebbe fallito o, peggio, sarebbe passato con un
    #   termine corrotto.**)*
    "        self._diag_ok_n = np.array(_ok_n, copy=True)",
    # ⚠ `W` E' LA STESSA ESPRESSIONE DELLA CURA: `bincount` di `w` su `i` e `j`. Se qui si
    #   scrivesse un'altra formula, la scomposizione parlerebbe di un'altra cura.
    "        self._diag_W = ((np.bincount(self.i, np.asarray(w, float), minlength=n)[:n]"
    " + np.bincount(self.j, np.asarray(w, float), minlength=n)[:n])"
    " if (w is not None and len(np.asarray(w)) == len(self.i)) else np.zeros(n))",
]
DIAG_CO = ["        self._diag_coppia = np.array(correzione, copy=True)"]


def copia_diag(sorgente, dest):
    """Genera la copia AL RUN e **pretende** che differisca solo per le righe dichiarate."""
    righe = io.open(sorgente, encoding="utf-8", newline="").read().split(NL)
    _pre_in = "        inerzia = np.maximum(_contrasto * _T2, 1e-6)"
    _pre_co = ("        omega_new = omega_src + dtn_c * (correzione / inerzia[:, None]"
               " - omega_src / _tau)")
    assert sum(1 for r in righe if r.startswith(_pre_in)) == 1, "ancora inerzia non unica"
    assert sum(1 for r in righe if r.startswith(_pre_co)) == 1, "ancora omega_new non unica"
    fuori, k = [], 0
    for r in righe:
        if r.startswith(_pre_co):
            fuori.extend(DIAG_CO)
            fuori.append(r)
            k += 1
            continue
        fuori.append(r)
        if r.startswith(_pre_in):
            fuori.extend(DIAG_IN)
            k += 1
    io.open(dest, "w", encoding="utf-8", newline=NL).write(NL.join(fuori))
    # LA POSTCONDIZIONE (`P9`)
    import difflib as _dl
    _dop = io.open(dest, encoding="utf-8", newline="").read().split(NL)
    _agg = [x[2:].rstrip(chr(13)) for x in _dl.ndiff(righe, _dop) if x.startswith("+ ")]
    _tol = [x[2:].rstrip(chr(13)) for x in _dl.ndiff(righe, _dop) if x.startswith("- ")]
    _est = [x for x in _agg if x not in set(DIAG_IN) | set(DIAG_CO)]
    assert not _est and not _tol, ("la copia differisce per righe NON dichiarate: "
                                  "aggiunte %r  tolte %r" % (_est[:2], _tol[:2]))
    ast.parse(NL.join(_dop))
    return hashlib.sha1(io.open(dest, "rb").read()).hexdigest()[:8], k


COPIA = os.path.join(FUORI, "_sim_diag_scomp.py")
blob_copia, anc = copia_diag(SIM, COPIA)

_S0, ARGV = _cli_flag.argv_del_driver([], dest=os.path.join(TMP, "_scarto"))
ARGV = ARGV + ["--nodi", "0"]

FIGLIO = r'''
import datetime as _dt
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import _cli_flag
import _passo
_argv, _scart = _cli_flag.argv_per(SIM, ARGV)
S, _a = _cli_flag.carica_dal_cli(_argv, nome="sim_scomp", sim=SIM)
assert not getattr(S, "CONTRASTO_INTENSIVO", False), "il flag DEVE essere spento in questa lettura"
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
for _ in range(PASSI_PRIMA):
    _passo.passo_pieno(S, net)

n0 = int(net.n)
o = dict(SEME=SEME, n0=n0, blob_sim=BLOB_SIM, blob_copia=BLOB_COPIA,
         quando=_dt.datetime.now().isoformat(), flag=bool(getattr(S, "CONTRASTO_INTENSIVO", False)),
         completo=False, righe=[], maturi=[], esclusi=0, esclusi_perche=[])
nati = {}


def _dg(nome):
    return np.asarray(getattr(net, nome, []), float)


for _p in range(1, BUDGET + 1):
    _pre = int(net.n)
    _passo.passo_pieno(S, net)
    if int(net.n) > _pre:
        for _k in range(_pre, int(net.n)):
            nati[_k] = _p
    n = int(net.n)
    W = _dg("_diag_W"); CT = _dg("_diag_contrasto"); PQ = _dg("_diag_peq_nodo")
    RH = _dg("_diag_rho_s"); CO = _dg("_diag_coppia"); IN = _dg("_diag_inerzia")
    # ❌❌ **SECONDO DIFETTO RILEVATO DA LUCA:** buttare il passo intero quando le
    #   diagnostiche sono corte **scarta OGNI PASSO CON UNA NASCITA** — le diagnostiche si
    #   scrivono in `step()`, la mitosi viene **dopo**, quindi `net.n > len(diag)` a ogni
    #   nascita. **MISURATO nel primo giro: 51 e 46 passi su 120 scartati, il 40 %**, e
    #   restavano **solo i passi senza nascite**: un campione DISTORTO proprio sul fenomeno
    #   che si vuole misurare.
    # ✅ **ORA: si usano i primi `len(diag)` nodi e si saltano SOLO i neonati di quel passo**
    #   (come faceva il sigillo esteso), e **si conta quanti passi avevano nascite.**
    _nd = int(min(W.size, CT.size, PQ.size, RH.size, IN.size, CO.shape[0]))
    if _nd < 10:
        o["esclusi"] += 1
        o["esclusi_perche"].append([_p, "diagnostiche troppo corte", _nd, int(n)])
        continue
    if _nd < n:
        o["passi_con_nascite"] = o.get("passi_con_nascite", 0) + 1
    n = _nd
    cop = np.linalg.norm(CO[:n], axis=1)
    _tr = net._tempo_rampa()
    ramp = np.minimum(1.0, np.asarray(net.eta, float)[:n] / (np.asarray(_tr, float)[:n]
                                                            if np.ndim(_tr) else _tr))
    om = np.linalg.norm(np.asarray(net.omega_s, float), axis=1)[:n]
    gr = np.zeros(n, int)
    _i = np.asarray(net.i, int); _j = np.asarray(net.j, int)
    _m = (_i < n) & (_j < n)
    np.add.at(gr, _i[_m], 1); np.add.at(gr, _j[_m], 1)
    # I MATURI DELLO STESSO PASSO: i nodi che c'erano al passo zero (indici < n0)
    mv = np.arange(min(n0, n))
    # ❌❌ **DIFETTO RILEVATO DA LUCA sul file committato, PRIMA che i dati fossero letti:**
    #   con le MEDIANE prese separatamente, `c_m != rho_m/peq_m` — **la mediana di un rapporto
    #   NON e' il rapporto delle mediane** — e l'identita' `T1+T2+T3 = log(c_f/c_m)` la
    #   richiede. **`K1` avrebbe fallito PER COSTRUZIONE, anche su dati perfetti**, e io
    #   avrei cercato il difetto nella raccolta.
    # ✅ **ORA: MEDIA DEI LOGARITMI (media geometrica).** `log` di una media geometrica e'
    #   **ADDITIVO**, quindi `mean(log c) = mean(log rho) - mean(log peq)` **esattamente**,
    #   nodo per nodo — e `K1` diventa un **controllo VERO** *(«il contrasto e' davvero
    #   `rho/peq` nodo per nodo?»)* invece di una tautologia rovesciata.
    #   ⚠ Si tengono solo i nodi con **tutte e quattro** le grandezze positive: dove `_ok_n`
    #     e' falso `_contrasto` vale `1` per CONVENZIONE, e li' l'identita' **non deve**
    #     chiudere. **Quanti se ne scartano E' UN NUMERO CHE VA NEL REFERTO.**
    OK_N = np.asarray(getattr(net, "_diag_ok_n", np.ones(n, bool)))[:n].astype(bool)
    _bm = (W[mv] > 0) & (PQ[mv] > 0) & (RH[mv] > 0) & (CT[mv] > 0) & OK_N[mv]
    _mv = mv[_bm]
    o["ok_n_falsi_maturi"] = o.get("ok_n_falsi_maturi", 0) + int(np.sum(~OK_N[mv]))
    if _mv.size < 10:
        o["esclusi"] += 1
        o["esclusi_perche"].append([_p, "meno di 10 maturi utilizzabili", int(_mv.size)])
        continue
    _wm = float(np.exp(np.mean(np.log(W[_mv]))))
    _pm = float(np.exp(np.mean(np.log(PQ[_mv]))))
    _rm = float(np.exp(np.mean(np.log(RH[_mv]))))
    _cm = float(np.exp(np.mean(np.log(CT[_mv]))))
    o.setdefault('scartati_maturi', []).append([_p, int(mv.size - _mv.size), int(mv.size)])
    # LE MEDIANE SI RIPORTANO A PARTE, come DESCRIZIONE (richiesta di Luca): servono a
    #   leggere l'ordine di grandezza, non a costruire l'identita'.
    o.setdefault('maturi_mediane', []).append(
        [_p, float(np.median(W[_mv])), float(np.median(PQ[_mv])), float(np.median(RH[_mv])),
         float(np.median(CT[_mv]))])
    if not (_wm > 0 and _pm > 0 and _rm > 0 and _cm > 0):
        # ⚠ NON si aggira con un `max(..., 1e-9)` (`A11`): il passo si ESCLUDE e SI CONTA.
        o["esclusi"] += 1
        o["esclusi_perche"].append([_p, "riferimento non positivo", _wm, _pm, _rm, _cm])
        continue
    o["maturi"].append([_p, _wm, _pm, _rm, _cm, float(np.median(cop[mv])),
                        float(np.median(om[mv])), float(np.median(gr[mv])),
                        float(np.median(ramp[mv]))])
    for _k, _nasc in nati.items():
        _e = _p - _nasc
        if _k >= n or _e < 1 or _e > ETA_MAX:
            continue
        if not OK_N[_k]:
            # il nodo porta il `_contrasto` DI CONVENZIONE (`= 1`): **si esclude e si
            #   CONTA**, non si lascia entrare nell'identita'.
            o["ok_n_falsi_figli"] = o.get("ok_n_falsi_figli", 0) + 1
            continue
        o["righe"].append([_p, int(_k), int(_e), float(W[_k]), float(PQ[_k]), float(RH[_k]),
                           float(CT[_k]), float(cop[_k]), float(om[_k]), float(ramp[_k]),
                           int(gr[_k]), float(IN[_k]),
                           _wm, _pm, _rm, _cm])
o["nati"] = len(nati)
o["completo"] = True
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  nati %d  righe %d  maturi %d  esclusi %d"
      % (NOME, len(nati), len(o["righe"]), len(o["maturi"]), o["esclusi"]))
'''


def riusabile(nome):
    p = os.path.join(TMP, nome + ".json")
    if not os.path.exists(p):
        return False, "assente"
    try:
        o = json.loads(io.open(p, encoding="utf-8").read())
    except Exception as e:
        return False, "illeggibile (%s)" % str(e)[:40]
    if not o.get("completo"):
        return False, "INCOMPLETO"
    if o.get("blob_sim") != blob_vero or o.get("blob_copia") != blob_copia:
        return False, ("BLOB DIVERSO: %s/%s contro %s/%s"
                       % (o.get("blob_sim"), o.get("blob_copia"), blob_vero, blob_copia))
    return True, o


def braccio(nome, seme):
    testa = ["RAD = %r" % RADICE, "TMPD = %r" % TMP, "NOME = %r" % nome, "SEME = %d" % seme,
             "SEP = %r" % SEP, "SIM = %r" % COPIA, "PASSI_PRIMA = %d" % PASSI_PRIMA,
             "BUDGET = %d" % BUDGET, "ETA_MAX = %d" % ETA_MAX, "ARGV = %r" % ARGV,
             "BLOB_SIM = %r" % blob_vero, "BLOB_COPIA = %r" % blob_copia, ""]
    p = os.path.join(TMP, "_br_%s.py" % nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(NL.join(testa) + FIGLIO)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# ==========================================================================================
# IL COLLAUDO (`P1-sexies`): su dati SINTETICI con `contrasto == rho/peq` nodo per nodo,
#   `K1` **deve PASSARE** con la media geometrica e **FALLIRE** con le mediane separate.
#   **Se non fallisce, il collaudo e' VUOTO e lo si dichiara.**
# ------------------------------------------------------------------------------------------
def collaudo_k1(seme=7, quanti=400):
    """Due risposte NOTE: geometrica -> chiude; mediane separate -> NON chiude."""
    rg = np.random.default_rng(seme)
    # i MATURI: `rho` e `peq` log-normali INDIPENDENTI, cosi' la mediana del rapporto e'
    #   diversa dal rapporto delle mediane (se fossero proporzionali, il difetto non si
    #   vedrebbe: **il caso sintetico deve CONTENERE il difetto**, non spiegarlo).
    rho_m = np.exp(rg.normal(0.0, 1.0, quanti))
    peq_m = np.exp(rg.normal(0.0, 1.0, quanti))
    W_m = np.exp(rg.normal(0.0, 0.5, quanti))
    ct_m = rho_m / peq_m                      # ESATTAMENTE, nodo per nodo
    rho_f = np.exp(rg.normal(-6.0, 1.0, 40))
    peq_f = np.exp(rg.normal(0.3, 0.2, 40))
    W_f = np.exp(rg.normal(-1.5, 0.4, 40))
    ct_f = rho_f / peq_f
    # ⚠ **I NODI DI CONVENZIONE**, richiesta di Luca: `contrasto = 1` con `rho/peq != 1`.
    #   Col filtro VECCHIO («tutte positive») **entrano**, e `K1` DEVE fallire; con `_ok_n`
    #   si escludono, e `K1` DEVE passare. **Sono il caso che deve FALLIRE.**
    rho_c = np.exp(rg.normal(-8.0, 0.5, 12))
    peq_c = np.exp(rg.normal(0.3, 0.2, 12))
    ct_c = np.ones(12)                      # LA CONVENZIONE: 1, e `1` e' POSITIVO
    ok_n_c = np.zeros(12, bool)             # `_ok_n` falso proprio su questi
    fuori = {}
    for modo in ('geometrica', 'mediane'):
        if modo == 'geometrica':
            g = lambda x: float(np.exp(np.mean(np.log(x))))
        else:
            g = lambda x: float(np.median(x))
        _r, _p, _w, _c = g(rho_m), g(peq_m), g(W_m), g(ct_m)
        for filtro in ('ok_n', 'tutte_positive'):
            if filtro == 'ok_n':
                _rf, _pf, _wf, _cf = rho_f, peq_f, W_f, ct_f
            else:
                # il filtro VECCHIO lascia entrare i nodi di CONVENZIONE
                _rf = np.concatenate([rho_f, rho_c]); _pf = np.concatenate([peq_f, peq_c])
                _wf = np.concatenate([W_f, np.exp(rg.normal(-1.5, 0.4, 12))])
                _cf = np.concatenate([ct_f, ct_c])
            tot = np.log(_cf / _c)
            T1 = np.log((_rf / _wf ** 2) / (_r / _w ** 2))
            T2 = 2.0 * np.log(_wf / _w)
            T3 = -np.log(_pf / _p)
            fuori[modo + '|' + filtro] = float(np.abs(T1 + T2 + T3 - tot).max())
    return fuori


_CO = collaudo_k1()
# QUATTRO celle, e servono tutte e quattro: la geometrica col filtro `_ok_n` DEVE chiudere,
#   e le altre tre DEVONO fallire — le mediane per l'aggregazione, il filtro vecchio per i
#   nodi di convenzione. **Se una delle tre non fallisce, il collaudo e' VUOTO in quella
#   cella e lo si dichiara.**
_CO_OK = (_CO['geometrica|ok_n'] < 1e-12
          and _CO['mediane|ok_n'] > 1e-3
          and _CO['geometrica|tutte_positive'] > 1e-3
          and _CO['mediane|tutte_positive'] > 1e-3)

LOG, RIPRESI, dati = [], {}, {}
proc = {}
for s in SEMI:
    nome = "scomp_s%d" % s
    ok, res = riusabile(nome)
    if ok:
        dati[nome] = res
        RIPRESI[nome] = (res.get("quando"), res.get("blob_sim"), res.get("blob_copia"))
        LOG.append("[%s] RIPRESO dal %s (blob %s/%s)"
                   % (nome, res.get("quando"), res.get("blob_sim"), res.get("blob_copia")))
        continue
    LOG.append("[%s] si gira: %s" % (nome, res))
    proc[nome] = braccio(nome, s)
for nome, pr in proc.items():
    so, se = pr.communicate()
    LOG.append("[%s] rc=%d %s" % (nome, pr.returncode,
                                  (so or b"").decode("utf-8", "replace").strip()[-110:]))
    if pr.returncode:
        LOG.append((se or b"").decode("utf-8", "replace")[-1500:])
    else:
        ok, res = riusabile(nome)
        if ok:
            dati[nome] = res

R = []


def P(s=""):
    R.append(s)


P("=" * 112)
P("LA SCOMPOSIZIONE ESATTA DEL DIVARIO DEI FIGLI   (2026-09-26)")
P("=" * 112)
P()
for l in LOG:
    P(l)
P()
P("blob del simulatore  %s      blob della copia  %s   (%d ancore, GENERATA AL RUN)"
  % (blob_vero, blob_copia, anc))
P("semi %s   flag SPENTO   passi pieni prima %d   budget %d   eta' fino a %d"
  % (SEMI, PASSI_PRIMA, BUDGET, ETA_MAX))
P()
# `P5`: LA CONFIGURAZIONE INTERA. Questo strumento **fa girare il simulatore**, quindi non e'
#   un caso da esenzione: **e' il caso per cui `P5` esiste.** Il presidio ha rifiutato il
#   primo commit di questo file, e aveva ragione.
_Sq, _ = _cli_flag.carica_dal_cli(_cli_flag.argv_per(COPIA, ARGV)[0], nome="cfg_scomp",
                                  sim=COPIA)
_cli_flag.dichiara_configurazione(_Sq, P)
if RIPRESI:
    P()
    P("BRACCI RIPRESI DA UN GIRO PRECEDENTE:")
    for _n in sorted(RIPRESI):
        P("  %-14s %s   blob %s/%s" % ((_n,) + RIPRESI[_n]))
P()

if not dati:
    P("STOP: nessun dato.")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL.join(R))
    sys.exit(1)

# ====================================================================== `K1`: l'identita' CHIUDE?
P("=" * 112)
P("IL COLLAUDO DI `K1` SU DATI SINTETICI A RISPOSTA NOTA (`P1-sexies`)")
P("=" * 112)
P("  dati con `contrasto == rho/peq` nodo per nodo, `rho` e `peq` log-normali INDIPENDENTI")
P("  (se fossero proporzionali il difetto non si vedrebbe: **il caso sintetico deve")
P("  CONTENERE il difetto**, non spiegarlo).")
P()
P("  %-34s %-14s %s" % ("aggregazione | filtro", "scarto max", "atteso"))
for _k4, _atteso in (("geometrica|ok_n", "~0  <- L'UNICO che deve chiudere"),
                     ("mediane|ok_n", ">> 0  (aggregazione sbagliata)"),
                     ("geometrica|tutte_positive", ">> 0  (nodi di CONVENZIONE dentro)"),
                     ("mediane|tutte_positive", ">> 0  (entrambi i difetti)")):
    P("  %-34s %-14.3e %s" % (_k4, _CO[_k4], _atteso))
P()
if _CO_OK:
    P("  -> COLLAUDO 4/4: chiude SOLO `geometrica|ok_n`.")
    P("     **Quindi `K1` e' un controllo VERO**: se fallisce sul dato, il difetto e' nella")
    P("     RACCOLTA, non nell'aggregazione.")
else:
    P("  -> ⛔ **COLLAUDO VUOTO O SBAGLIATO, e lo dichiaro invece di proseguire:**")
    for _k4 in sorted(_CO):
        P("     %-34s %.3e" % (_k4, _CO[_k4]))
    P("     Se le mediane NON fanno fallire l'identita', questo collaudo non prova niente,")
    P("     e `K1` resta una tautologia travestita.")
P()
P("=" * 112)
P("`K1` -- L'IDENTITA' CHIUDE?   |T1+T2+T3 - log(c_f/c_m)| < 1e-9")
P("=" * 112)
_k1_max, _k1_n = 0.0, 0
SC = {}
for nome, o in sorted(dati.items()):
    ar = np.array(o["righe"], float)
    if not ar.size:
        continue
    # [passo, id, eta, W, peq, rho, contr, coppia, omega, ramp, grado, inerzia, Wm, pm, rm, cm]
    W, pq, rh, ct = ar[:, 3], ar[:, 4], ar[:, 5], ar[:, 6]
    Wm, pm, rm, cm = ar[:, 12], ar[:, 13], ar[:, 14], ar[:, 15]
    buono = (W > 0) & (pq > 0) & (rh > 0) & (ct > 0)
    ar, W, pq, rh, ct = ar[buono], W[buono], pq[buono], rh[buono], ct[buono]
    Wm, pm, rm, cm = Wm[buono], pm[buono], rm[buono], cm[buono]
    tot = np.log(ct / cm)
    T1 = np.log((rh / W ** 2) / (rm / Wm ** 2))
    T2 = 2.0 * np.log(W / Wm)
    T3 = -np.log(pq / pm)
    res = np.abs(T1 + T2 + T3 - tot)
    _k1_max = max(_k1_max, float(res.max()))
    _k1_n += int(res.size)
    SC[nome] = (ar, tot, T1, T2, T3)
    P("  %-14s campioni %6d   scarto massimo dell'identita'  %.3e"
      % (nome, int(res.size), float(res.max())))
P()
_K1 = _k1_max < 1e-9
P("  -> `K1` %s   (massimo su %d campioni: %.3e)"
  % ("PASS" if _K1 else "FAIL", _k1_n, _k1_max))
if not _K1:
    P()
    P("  ⛔ **STOP: LA RACCOLTA E' INCOERENTE, E NESSUNA FRAZIONE SI PUBBLICA.**")
    P("  Se l'identita' non chiude, `rho`, `peq` o `W` sono stati letti in momenti diversi.")
    P("  *(Era il presidio scritto PRIMA: tre frazioni sono numeri belli e convincenti, e")
    P("  pubblicarli da una raccolta sfasata sarebbe il peggio che si possa fare qui.)*")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL.join(R))
    sys.exit(1)
P()

# ====================================================================== le tre frazioni
P("=" * 112)
P("LE TRE FRAZIONI, ETA' PER ETA' -- figlio contro MATURI DELLO STESSO PASSO")
P("=" * 112)
P("  T2 = quello che `rho_s/W^2` TOGLIE      T3 = quello che resta a `peq` EREDITATO")
P("  T1 = quello che resta in `rho/W^2` a parita' di peso: NESSUNA delle due cure lo tocca")
P()
FRAZ = {}
for nome, (ar, tot, T1, T2, T3) in sorted(SC.items()):
    P("-" * 112)
    P("%s   (nati %d)" % (nome, dati[nome].get("nati")))
    P("%-6s %-7s %-12s %-12s %-12s %-12s %-9s %-9s %s"
      % ("eta", "campioni", "c_f/c_m", "log(c_f/c_m)", "T1", "T2", "T3", "%T2", "%T3   %T1"))
    et = sorted(set(int(x) for x in ar[:, 2]))
    fr = {}
    for e in et:
        m = ar[:, 2] == e
        # ❌ **SECONDO DIFETTO RILEVATO DA LUCA:** prendere la MEDIANA di `T1`, `T2`, `T3`
        #   separatamente e normalizzare sulla loro somma fa sommare le frazioni al 100 %
        #   **per costruzione**, e **nasconde la non-additivita'**.
        # ✅ **ORA SI FA LA MEDIA** dei tre termini (sono gia' LOGARITMI: la media di un
        #   logaritmo E' il logaritmo della media geometrica, e **la somma si conserva**).
        #   Cosi' `_a + _b + _c` e' la media di `T1+T2+T3`, che `K1` ha verificato essere
        #   **uguale** alla media di `log(c_f/c_m)`: le frazioni sommano al 100 % **perche'
        #   l'identita' chiude sul DATO**, non perche' le ho normalizzate.
        _t = float(np.mean(tot[m]))
        _a, _b, _c = float(np.mean(T1[m])), float(np.mean(T2[m])), float(np.mean(T3[m]))
        _s = _a + _b + _c
        assert abs(_s - _t) < 1e-9, (
            "l'additivita' non tiene sull'aggregato: eta %d, %.3e" % (e, abs(_s - _t)))
        f2 = 100.0 * _b / _s if _s else float("nan")
        f3 = 100.0 * _c / _s if _s else float("nan")
        f1 = 100.0 * _a / _s if _s else float("nan")
        fr[e] = (f1, f2, f3, _t)
        P("%-6d %-7d %-12.4g %-12.4f %-12.4f %-12.4f %-9.4f %-9.1f %-6.1f %.1f"
          % (e, int(m.sum()), float(np.median(np.exp(tot[m]))), _t, _a, _b, _c, f2, f3, f1))
    FRAZ[nome] = fr
    P()

# ====================================================================== `K2`
P("=" * 112)
P("`K2` -- LE FRAZIONI SONO LE STESSE SUI DUE SEMI?")
P("=" * 112)
_nomi = sorted(FRAZ)
_K2 = True
if len(_nomi) >= 2:
    a, b = FRAZ[_nomi[0]], FRAZ[_nomi[1]]
    P("%-6s %-22s %-22s %s" % ("eta", "%T2 (s1 / s2)", "%T3 (s1 / s2)", "segni concordi?"))
    for e in sorted(set(a) & set(b)):
        c1 = (a[e][1] > 0) == (b[e][1] > 0)
        c2 = (a[e][2] > 0) == (b[e][2] > 0)
        _K2 = _K2 and c1 and c2
        P("%-6d %-22s %-22s %s"
          % (e, "%.1f / %.1f" % (a[e][1], b[e][1]), "%.1f / %.1f" % (a[e][2], b[e][2]),
             "si" if (c1 and c2) else "NO"))
else:
    _K2 = False
    P("  un solo seme utilizzabile: `K2` NON MISURATO.")
P()
P("  -> `K2` %s" % ("PASS" if _K2 else "FAIL / NON MISURATO"))
P()

# ====================================================================== `K3`: coppia ~ ramp^c
P("=" * 112)
P("`K3` (`R3bis`) -- LA COPPIA SUI FIGLI: `coppia ~ ramp^c`")
P("=" * 112)


def pend(x, y):
    x = np.log(np.asarray(x, float))
    y = np.asarray(y, float)
    m = np.isfinite(y) & (y > 0) & np.isfinite(x)
    if m.sum() < 3:
        return float("nan"), float("nan"), int(m.sum())
    c = np.polyfit(x[m], np.log(y[m]), 1)
    yy = np.polyval(c, x[m])
    r2 = 1.0 - np.sum((np.log(y[m]) - yy) ** 2) / max(
        np.sum((np.log(y[m]) - np.mean(np.log(y[m]))) ** 2), 1e-300)
    return float(c[0]), float(r2), int(m.sum())


P("%-14s %-16s %-12s %-10s %s" % ("braccio", "grandezza", "esponente", "R2", "punti"))
_K3 = []
for nome, (ar, tot, T1, T2, T3) in sorted(SC.items()):
    et = sorted(set(int(x) for x in ar[:, 2]))
    rr = [float(np.median(ar[ar[:, 2] == e, 9])) for e in et]
    for _i, _nm in ((7, "coppia"), (8, "|omega|"), (5, "rho"), (3, "W"), (11, "inerzia")):
        yy = [float(np.median(ar[ar[:, 2] == e, _i])) for e in et]
        c, r2, npt = pend(rr, yy)
        P("%-14s %-16s %-12.4f %-10.4f %d" % (nome, _nm, c, r2, npt))
        if _nm == "coppia":
            _K3.append((nome, c, r2, npt))
    P("%-14s %-16s %s" % (nome, "ramp (da->a)", "%.4g -> %.4g" % (rr[0], rr[-1])))
    P()
_ok3 = bool(_K3) and all(abs(c - 1.0) <= 0.3 for _n, c, _r, _p in _K3 if c == c)
_zero3 = bool(_K3) and all(abs(c) <= 0.3 for _n, c, _r, _p in _K3 if c == c)
P("  -> `K3`: %s"
  % ("l'ASIMMETRIA E' CONFERMATA (`c ~ 1` entro 0.3)" if _ok3
     else ("LA COPPIA NON PORTA `ramp` (`c ~ 0`): `R3bis` CADE" if _zero3
           else "`c` NON e' ne' 1 ne' 0: **`R3bis` RESTA APERTO**, e il numero e' qui sopra")))
P()

# ====================================================================== `K4`: il nullo
P("=" * 112)
P("`K4` -- IL NULLO: i MATURI, e la loro DERIVA nel budget")
P("=" * 112)
P("%-14s %-13s %-13s %-13s %-13s %s" % ("braccio", "W", "peq", "rho", "contrasto", "|omega|"))
for nome, o in sorted(dati.items()):
    mm = np.array(o["maturi"], float)
    if not mm.size:
        continue
    P("%-14s %-13s %-13s %-13s %-13s %s"
      % (nome + " inizio", "%.4g" % mm[0, 1], "%.4g" % mm[0, 2], "%.4g" % mm[0, 3],
         "%.4g" % mm[0, 4], "%.4g" % mm[0, 6]))
    P("%-14s %-13s %-13s %-13s %-13s %s"
      % (nome + " fine", "%.4g" % mm[-1, 1], "%.4g" % mm[-1, 2], "%.4g" % mm[-1, 3],
         "%.4g" % mm[-1, 4], "%.4g" % mm[-1, 6]))
P()
P("  I maturi DERIVANO, ed e' la ragione per cui il confronto e' allo STESSO PASSO: un")
P("  riferimento fisso darebbe un divario che cambia **perche' cambia il riferimento**.")
P("  passi con NASCITE (diagnostiche corte, neonati saltati): %s"
  % {n: o.get("passi_con_nascite", 0) for n, o in sorted(dati.items())})
P("  nodi con `_ok_n` FALSO esclusi -- maturi: %s   figli: %s"
  % ({n: o.get("ok_n_falsi_maturi", 0) for n, o in sorted(dati.items())},
     {n: o.get("ok_n_falsi_figli", 0) for n, o in sorted(dati.items())}))
P("  *(sono i nodi col `_contrasto` DI CONVENZIONE: 1. Positivo, quindi il filtro")
P("  «tutte positive» NON li toglieva.)*")
P("  passi ESCLUSI e il perche': %s"
  % {n: (o.get("esclusi"), (o.get("esclusi_perche") or [])[:2]) for n, o in sorted(dati.items())})
P()

P("=" * 112)
P("LA RISPOSTA ALLA DOMANDA DI LUCA")
P("=" * 112)
if FRAZ:
    _e_ult = max(min(FRAZ[n]) for n in FRAZ), max(max(FRAZ[n]) for n in FRAZ)
    for nome in sorted(FRAZ):
        fr = FRAZ[nome]
        e0, e1 = min(fr), max(fr)
        P("  %-14s eta' %d:  T2 %.1f %%   T3 %.1f %%   T1 %.1f %%"
          % (nome, e0, fr[e0][1], fr[e0][2], fr[e0][0]))
        P("  %-14s eta' %d: T2 %.1f %%   T3 %.1f %%   T1 %.1f %%"
          % ("", e1, fr[e1][1], fr[e1][2], fr[e1][0]))
P()
P("  **`rho_s/W^2` toglie la quota `T2`. `peq` alla nascita toglie `T3`. `T1` non lo tocca")
P("  nessuna delle due.** Le tre sommano a 100 % **per identita'**, non per costruzione del")
P("  criterio: `K1` lo verifica sul dato.")
P()
P("COSA QUESTA LETTURA *NON* DICE:")
P("  - **quale cura scegliere: decide Luca.** Qui ci sono le frazioni.")
P("  - **non dice che `rho_s/W^2` sia sicura:** toglie `T2` per costruzione, ma non e' misurato")
P("    che non rompa altro (`rho_s` entra in `lambda_nodi`, nella soglia della mitosi, nella")
P("    coppia Schwinger: `doc/LETTURE_rho_s.md`).")
P("  - **niente sul taglio:** questa e' la famiglia dei FIGLI.")
P("  - le mediane per eta' mescolano figli di madri diverse: le frazioni sono di POPOLAZIONE.")
P("  - DUE SEMI: `K2` guarda la concordanza, non una barra (per una barra servono >= 4).")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
sys.exit(0 if (_K1 and _K2 and _CO_OK) else 1)
