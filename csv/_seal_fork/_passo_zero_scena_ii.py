# -*- coding: utf-8 -*-
"""SCENA `(ii)` -- **LA PARTE AL PASSO ZERO**, che non dipende dalla mitosi.

> **Decisione di Luca, 2026-09-25: il giro di 120 passi e' SOSPESO** finche' la soglia della
> mitosi non e' una legge derivata *(`3pi` e' un numero tarato a posteriori nell'epoca 1)*.
> **Questa parte si fa subito**, perche' **non dipende dalla mitosi**.

**COSA MISURA, e da dove viene ogni voce** *(letta dalla scheda, non dalla memoria)*:

```
S2   min distanza fra POSIZIONI >= LAM          (cKDTree, k=2)  -- `A13` misurato
S3   sum(d < LAM) == 0  E  sum(d == LAM) == 0   -- i due INSIEME
S4   `_g_sm_nascite` == 0 al passo zero         -- il presidio non deve scattare
S5   nodi isolati == 0
S6   d == |pos_i - pos_j| per OGNI arco         -- `D02` a questo sito
S9   intensita' media DENTRO le regioni / quella del VUOTO,  > 1, col VALORE
S10(0) frazione della coorte con I > Lam, al passo ZERO, PIU' il profilo PER GUSCI
     contati in ARCHI dal nucleo, PIU' il braccio di controllo a FASI CASUALI
P1-P5  le previsioni analitiche, verificate al passo zero
ARCHI  il numero, e la FRAZIONE DI ARCHI SOTTO `2 LAM`  (`U2c`, passo 0)
U2a/b  i contatori di `_nasce` per grandezza e per sito
```

**`S1` NON si rifa' qui:** e' la byte-identita' a flag spento, **gia' sigillata** da
`_c1_semina_lam.py` *(`C1` PASS PIENO: 218 uguali / 0 diversi / 0 non confrontati)*. **Rifarla
sarebbe un secondo criterio sulla stessa cosa**, e va detto invece di contarla due volte.
**`S7` E' IL GIRO: SOSPESO.** **`S8` NON ESISTE nella scheda** -- la numerazione del mandato
salta da `S7` a `S9`, e lo dico invece di inventarne uno.

**Un processo per braccio** *(`STANDARD 1`)*. ASCII puro nel sorgente; l'output e' UTF-8.
"""
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
FUORI = os.path.join(_QUI, "_sig_scena_ii")
DEST = os.path.join(FUORI, "PASSO_ZERO_scena_ii.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEMI = [11, 12, 13, 14]          # >= 4 semi: `P3` del par.0-ter (con 2, t(0.025,1) = 12.706)

FIGLIO = r'''
import io, json, os, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, RAD)
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sim_z", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = bool(SEMLAM)
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = int(NODI)
S._MC_VIDEO["fasi_casuali"] = bool(CASUALI)
S._semina_masse_coerenti()
net = S.net
LAM = float(S.LAM)
pos = np.asarray(net.pos, float)
d = np.asarray(net.d, float)
ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
co = S.test["dati"]["coorti"]
o = dict(SEME=SEME, SEP=float(SEP), SEMINA_LAM=bool(SEMLAM), CASUALI=bool(CASUALI),
         LAM=LAM, n=int(net.n), archi=int(d.size))
o.update(S.test["dati"]["scena_ii"])

# ---- S2 : distanza minima fra POSIZIONI (non fra archi) -----------------------------------
o["S2_min_dist"] = float(cKDTree(pos).query(pos, k=2)[0][:, 1].min())

# ---- S3 : `d` sotto e A `LAM` --------------------------------------------------------------
o["S3_sotto"] = int(np.sum(d < LAM)); o["S3_a_lam"] = int(np.sum(d == LAM))
o["d_min"] = float(d.min()) if d.size else float("nan")

# ---- S4 : il presidio non deve scattare ----------------------------------------------------
o["S4_nascite"] = int(getattr(net, "_g_sm_nascite", 0))

# ---- S5 : nodi isolati ---------------------------------------------------------------------
grado = np.zeros(net.n, int)
np.add.at(grado, ii, 1); np.add.at(grado, jj, 1)
o["S5_isolati"] = int(np.sum(grado == 0)); o["grado_medio"] = float(grado.mean())

# ---- S6 : `d` contro il DISEGNO ------------------------------------------------------------
geo = np.linalg.norm(pos[ii] - pos[jj], axis=1)
o["S6_max_scarto"] = float(np.max(np.abs(d - geo))) if d.size else 0.0
o["S6_frazione_diversi"] = float(np.mean(np.abs(d - geo) > 1e-12)) if d.size else 0.0

# ---- ARCHI : la frazione sotto `2 LAM`  (`U2c`, passo 0) ------------------------------------
o["U2c_sotto_2lam"] = float(np.mean(d < 2.0 * LAM)) if d.size else float("nan")
o["d_mediana"] = float(np.median(d)) if d.size else float("nan")
o["d_p05"] = float(np.percentile(d, 5)) if d.size else float("nan")

# ---- U2a/U2b : i contatori per grandezza e per sito ----------------------------------------
o["U2_contatori"] = {k: (float(v) if isinstance(v, float) else int(v))
                     for k, v in vars(net).items() if k.startswith("_sm_")}

# ---- S9 : intensita' DENTRO le regioni / nel VUOTO ----------------------------------------
I = np.asarray(net.intensita(), float)
dentro = np.concatenate([co["massa_%d" % k] for k in range(3)])
o["S9_I_massa"] = float(I[dentro].mean()); o["S9_I_vuoto"] = float(I[co["vuoto"]].mean())
o["S9_contrasto"] = (o["S9_I_massa"] / o["S9_I_vuoto"]) if o["S9_I_vuoto"] else float("inf")
for k in range(3):
    o["S9_I_massa_%d" % k] = float(I[co["massa_%d" % k]].mean())

# ---- `Lam` : la scala RELAZIONALE, `mean(I)` (la stessa di `cs_floor`) ---------------------
o["P3_Lam"] = float(I.mean())

# ---- S10 al passo ZERO : frazione della coorte con `I > Lam` -------------------------------
_L = o["P3_Lam"]
o["S10_frazione"] = {("massa_%d" % k): float(np.mean(I[co["massa_%d" % k]] > _L))
                     for k in range(3)}
o["S10_frazione"]["vuoto"] = float(np.mean(I[co["vuoto"]] > _L))

# ---- S10 : il PROFILO PER GUSCI, contati in ARCHI dal nucleo (non da `pos`) -----------------
# BFS sul grafo: il "nucleo" e' il nodo della regione piu' vicino al centro, e il guscio e'
# la DISTANZA IN ARCHI. Luca: "contati in ARCHI dal nucleo della regione (non da `pos`)".
import collections
adj = collections.defaultdict(list)
for _a, _b in zip(ii, jj):
    adj[_a].append(_b); adj[_b].append(_a)
prof = {}
for k in range(3):
    idx = co["massa_%d" % k]
    if not len(idx):
        continue
    ang = 2.0 * np.pi * k / 3.0
    c = np.array([float(SEP) * np.cos(ang), float(SEP) * np.sin(ang), 0.0])
    radice = int(idx[np.argmin(np.linalg.norm(pos[idx] - c, axis=1))])
    insieme = set(int(x) for x in idx)
    dist = {radice: 0}
    q = collections.deque([radice])
    while q:
        u = q.popleft()
        for v in adj[u]:
            v = int(v)
            if v in insieme and v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    gusci = collections.defaultdict(list)
    for v, g in dist.items():
        gusci[g].append(v)
    prof["massa_%d" % k] = {
        "raggiunti": len(dist), "totale": int(len(idx)),
        "gusci": {str(g): [len(v), float(np.mean(I[np.array(v)] > _L))]
                  for g, v in sorted(gusci.items())}}
o["S10_profilo_archi"] = prof

# ---- P1 : somma dei PESI per nodo, `exp(-d/LAM)` -------------------------------------------
w = np.exp(-d / LAM)
sw = np.zeros(net.n)
np.add.at(sw, ii, w); np.add.at(sw, jj, w)
o["P1_pesi_per_nodo"] = float(np.median(sw))

# ---- P4 : `cs_floor` dentro le masse -------------------------------------------------------
try:
    cs = np.asarray(net.cs_floor(), float) if hasattr(net, "cs_floor") else None
except Exception:
    cs = None
if cs is None:
    o["P4_cs_massa"] = None; o["P4_cs_vuoto"] = None; o["P4_nota"] = "cs_floor non esposto"
else:
    o["P4_cs_massa"] = float(np.median(cs[dentro])) if cs.size >= net.n else None
    o["P4_cs_vuoto"] = float(np.median(cs[co["vuoto"]])) if cs.size >= net.n else None

# ---- P5 : `lambda_nodi`, quasi costante? ---------------------------------------------------
try:
    ln = np.asarray(net.lambda_nodi(), float)
    o["P5_lambda_med"] = float(np.median(ln)); o["P5_lambda_p05"] = float(np.percentile(ln, 5))
    o["P5_lambda_p95"] = float(np.percentile(ln, 95))
    o["P5_lambda_su_LAM"] = [o["P5_lambda_p05"] / LAM, o["P5_lambda_med"] / LAM,
                             o["P5_lambda_p95"] / LAM]
except Exception as e:
    o["P5_nota"] = "lambda_nodi: %s" % e

io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  n=%d archi=%d" % (NOME, net.n, d.size))
'''


def braccio(nome, sep, seme, semlam=True, casuali=False, nodi=0):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEP = %r\nSEME = %d\nSEMLAM = %r\n"
           "CASUALI = %r\nNODI = %d\n" % (RADICE, TMP, nome, sep, seme, semlam, casuali, nodi))
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src + FIGLIO)
    r = subprocess.run([sys.executable, p], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r


def leggi(nome):
    return json.loads(io.open(os.path.join(TMP, nome + ".json"), encoding="utf-8").read())


SCENE = [("a", 6.1158), ("b", 4.0)]
LOG = []
DATI = {}
for et, sep in SCENE:
    for seme in SEMI:
        nm = "%s_s%d" % (et, seme)
        rr = braccio(nm, sep, seme)
        LOG.append("[%s] rc=%d %s" % (nm, rr.returncode, (rr.stdout or "").strip()[-160:]))
        if rr.returncode:
            LOG.append((rr.stderr or "")[-1200:])
        else:
            DATI[nm] = leggi(nm)
    # BRACCIO DI CONTROLLO DI `S10`: fasi CASUALI dentro le regioni, STESSO seme
    nm = "%s_ctrl" % et
    rr = braccio(nm, sep, SEMI[0], casuali=True)
    LOG.append("[%s] rc=%d %s" % (nm, rr.returncode, (rr.stdout or "").strip()[-160:]))
    if rr.returncode:
        LOG.append((rr.stderr or "")[-1200:])
    else:
        DATI[nm] = leggi(nm)

P_ = []


def P(s=""):
    P_.append(s)


def crit(sigla, cosa, ok, detta):
    P("%-8s %-4s  %s" % (sigla, "PASS" if ok else "FAIL", cosa))
    for r_ in (detta or "").split(chr(10)):
        if r_:
            P("                " + r_)
    return bool(ok)


import numpy as np


def st(et, campo):
    v = [DATI["%s_s%d" % (et, s)][campo] for s in SEMI if "%s_s%d" % (et, s) in DATI]
    a = np.asarray(v, float)
    return a, float(a.mean()), (float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else float("nan"))


P("=" * 104)
P("SCENA (ii) -- IL PASSO ZERO. Il giro di 120 passi e' SOSPESO (decisione di Luca, 2026-09-25).")
P("=" * 104)
P()
for l in LOG:
    P(l)
P()
if len([k for k in DATI if k.endswith("_s%d" % SEMI[0])]) < 2:
    P("STOP: mancano bracci. Nessun criterio si legge.")
    io.open(DEST, "w", encoding="utf-8", newline="\n").write(chr(10).join(P_) + chr(10))
    print(chr(10).join(P_))
    sys.exit(1)

A = DATI["a_s%d" % SEMI[0]]
LAM = A["LAM"]
P("LAM = %.9f    R_CONN = %.9f    semi = %s" % (LAM, A["R_CONN"], SEMI))
P()
P("GEOMETRIA E TAGLIA (media su %d semi, con SE fra semi -- par.0-ter P3)" % len(SEMI))
P("  %-6s %-10s %-10s %-22s %-22s %-10s" % ("scena", "sep", "r_reg", "n (saturazione)",
                                            "ARCHI", "QUOTA"))
for et, sep in SCENE:
    n_, nm_, ns_ = st(et, "n")
    a_, am_, as_ = st(et, "archi")
    q_, qm_, qs_ = st(et, "quota")
    P("  %-6s %-10.4f %-10.6f %-22s %-22s %.6f +- %.6f"
      % (et, sep, DATI["%s_s%d" % (et, SEMI[0])]["r_regione"],
         "%.1f +- %.1f" % (nm_, ns_), "%.1f +- %.1f" % (am_, as_), qm_, qs_))
P()

OK = []

# ---------------------------------------------------------------- S2
_v = []
for et, _ in SCENE:
    a_, m_, s_ = st(et, "S2_min_dist")
    _v.append((et, a_.min(), m_))
OK.append(crit("S2", "min distanza fra POSIZIONI >= LAM (`A13` misurato)",
               all(x[1] >= LAM for x in _v),
               chr(10).join("scena (%s): min fra semi = %.9f   media = %.9f   LAM = %.9f"
                            % (x[0], x[1], x[2], LAM) for x in _v)))

# ---------------------------------------------------------------- S3
_v = [(et, st(et, "S3_sotto")[0].sum(), st(et, "S3_a_lam")[0].sum(), st(et, "d_min")[0].min())
      for et, _ in SCENE]
OK.append(crit("S3", "`sum(d < LAM) == 0` E `sum(d == LAM) == 0` -- i due INSIEME",
               all(x[1] == 0 and x[2] == 0 for x in _v),
               chr(10).join("scena (%s): sotto LAM = %d   A LAM = %d   min(d) = %.9f"
                            % (x[0], x[1], x[2], x[3]) for x in _v)
               + chr(10) + "lo ZERO sul secondo distingue \"non c'e' bisogno di troncare\" da \"troncato\""))

# ---------------------------------------------------------------- S4
_v = [(et, st(et, "S4_nascite")[0].sum()) for et, _ in SCENE]
OK.append(crit("S4", "`_g_sm_nascite == 0` al passo zero: il presidio NON scatta",
               all(x[1] == 0 for x in _v),
               chr(10).join("scena (%s): nascite = %d" % x for x in _v)))

# ---------------------------------------------------------------- S5
_v = [(et, st(et, "S5_isolati")[0].sum(), st(et, "grado_medio")[1]) for et, _ in SCENE]
OK.append(crit("S5", "nodi isolati == 0",
               all(x[1] == 0 for x in _v),
               chr(10).join("scena (%s): isolati = %d   grado medio = %.3f" % x for x in _v)))

# ---------------------------------------------------------------- S6
_v = [(et, st(et, "S6_max_scarto")[0].max(), st(et, "S6_frazione_diversi")[1]) for et, _ in SCENE]
OK.append(crit("S6", "`d == |pos_i - pos_j|` per OGNI arco al passo zero (`D02` a questo sito)",
               all(x[1] <= 1e-12 for x in _v),
               chr(10).join("scena (%s): max scarto = %.3e   frazione diversi = %.6f" % x
                            for x in _v)
               + chr(10) + "riferimento storico: divergeva sul 42.47 %"))

# ---------------------------------------------------------------- S9
_v = []
for et, _ in SCENE:
    c_, cm_, cs_ = st(et, "S9_contrasto")
    im_ = st(et, "S9_I_massa")[1]
    iv_ = st(et, "S9_I_vuoto")[1]
    _v.append((et, cm_, cs_, im_, iv_, c_.min()))
OK.append(crit("S9", "intensita' DENTRO le regioni / nel VUOTO > 1 -- IL CRITERIO CHE DECIDE SE LA STRADA (ii) ESISTE",
               all(x[5] > 1.0 for x in _v),
               chr(10).join("scena (%s): contrasto = %.4f +- %.4f   (min fra semi %.4f)"
                            "   I_massa = %.6e   I_vuoto = %.6e" % (x[0], x[1], x[2], x[5], x[3], x[4])
                            for x in _v)
               + chr(10) + "NON basta \"esiste un effetto\": 1.01 e 10 sono due fisiche diverse."))

# ---------------------------------------------------------------- S10 al passo zero + controllo
P()
P("-" * 104)
P("S10 AL PASSO ZERO -- frazione della coorte con `I > Lam`, e IL BRACCIO DI CONTROLLO")
P("-" * 104)
for et, _ in SCENE:
    D0 = DATI["%s_s%d" % (et, SEMI[0])]
    C0 = DATI.get("%s_ctrl" % et)
    P("scena (%s)   Lam = %.6e" % (et, D0["P3_Lam"]))
    for k in ("massa_0", "massa_1", "massa_2", "vuoto"):
        f = D0["S10_frazione"][k]
        fc = C0["S10_frazione"][k] if C0 else float("nan")
        P("   %-9s COERENTE %.4f     CONTROLLO (fasi casuali) %.4f     contrasto %s"
          % (k, f, fc, ("%.3f" % (f / fc)) if fc else "inf"))
    P("   PROFILO PER GUSCI, contati in ARCHI dal nucleo (non da `pos`):")
    for k in ("massa_0", "massa_1", "massa_2"):
        pr = D0["S10_profilo_archi"].get(k)
        if not pr:
            continue
        gg = "  ".join("g%s:n=%d,f=%.3f" % (g, v[0], v[1]) for g, v in sorted(
            pr["gusci"].items(), key=lambda z: int(z[0])))
        P("     %-9s raggiunti %d/%d   %s" % (k, pr["raggiunti"], pr["totale"], gg))
        if pr["raggiunti"] < pr["totale"]:
            P("       ! la regione NON e' connessa nel grafo: %d nodi non si raggiungono dal nucleo"
              % (pr["totale"] - pr["raggiunti"]))
    P()

# ---------------------------------------------------------------- ARCHI e U2c
P("-" * 104)
P("ARCHI, E LA FRAZIONE SOTTO `2 LAM` (`U2c` al passo 0) -- il secondo motore del gonfiamento")
P("-" * 104)
for et, _ in SCENE:
    a_, am_, as_ = st(et, "archi")
    u_, um_, us_ = st(et, "U2c_sotto_2lam")
    dm_ = st(et, "d_mediana")[1]
    dp_ = st(et, "d_p05")[1]
    P("  scena (%s): ARCHI = %.1f +- %.1f     sotto 2 LAM = %.4f +- %.4f"
      "     mediana(d) = %.4f = %.3f LAM     p05 = %.4f" % (et, am_, as_, um_, us_, dm_,
                                                            dm_ / LAM, dp_))
P("  (la stima di Luca per la voce `U2`/`M2` era `~1/4`: qui e' MISURATA, non assunta)")
P()
P("CONTATORI DI `_nasce` AL PASSO ZERO (devono essere assenti o nulli: `S4`)")
for et, _ in SCENE:
    P("  scena (%s): %s" % (et, DATI["%s_s%d" % (et, SEMI[0])]["U2_contatori"] or "NESSUNO"))
P()

# ---------------------------------------------------------------- P1-P5
P("-" * 104)
P("LE PREVISIONI `P1`-`P5`, verificate al passo zero. CRITERIO: uno scarto > FATTORE 2 va spiegato.")
P("-" * 104)
P("  ATTENZIONE: le previsioni VENGONO DAL MANDATO, non le ho derivate io (dichiarato nella scheda).")
P()
PREV = {"a": {"P1": 9.0, "P2": 27.0, "P3": 5.0, "P4": 0.55},
        "b": {"P1": 9.0, "P2": 27.0, "P3": 5.0, "P4": 0.55}}
for et, _ in SCENE:
    D0 = DATI["%s_s%d" % (et, SEMI[0])]
    p1 = st(et, "P1_pesi_per_nodo")[1]
    p2 = st(et, "S9_contrasto")[1]
    p3 = st(et, "P3_Lam")[1]
    P("  scena (%s)" % et)
    for sig, mis, att, nome in (("P1", p1, PREV[et]["P1"], "somma dei pesi per nodo (mediana)"),
                                ("P2", p2, PREV[et]["P2"], "contrasto I_massa/I_vuoto"),
                                ("P3", p3, PREV[et]["P3"], "Lam = mean(I)")):
        r = (mis / att) if att else float("inf")
        seg = "OK" if 0.5 <= r <= 2.0 else "!! FUORI DAL FATTORE 2"
        P("    %-4s %-38s misurato %-14.6g previsto %-8g  rapporto %.3f  %s"
          % (sig, nome, mis, att, r, seg))
    if D0.get("P4_cs_massa") is not None:
        P("    P4   cs_floor mediano: massa %.6f   vuoto %.6f   previsto ~%.2f"
          % (D0["P4_cs_massa"], D0["P4_cs_vuoto"], PREV[et]["P4"]))
    else:
        P("    P4   NON MISURATO: %s" % D0.get("P4_nota", "cs_floor non accessibile"))
    if "P5_lambda_su_LAM" in D0:
        q = D0["P5_lambda_su_LAM"]
        P("    P5   lambda_nodi / LAM:  p05 %.4f   mediana %.4f   p95 %.4f"
          % (q[0], q[1], q[2]))
        P("         previsto: QUASI COSTANTE fra 0.74 e 0.76 LAM.  escursione p95/p05 = %.4f"
          % (q[2] / q[0] if q[0] else float("inf")))
        P("         se e' quasi costante, la legge di schermatura e' di fatto SPENTA dalla")
        P("         soglia irraggiungibile -- lo stesso difetto di `massa_critica_collasso` (`U1`).")
    else:
        P("    P5   NON MISURATO: %s" % D0.get("P5_nota", "?"))
    P()

P("=" * 104)
P("ESITO DEI CRITERI DEL PASSO ZERO: %d/%d PASS" % (sum(1 for x in OK if x), len(OK)))
P("=" * 104)
P()
P("COSA QUESTO NON DICE, e va detto:")
P("  - `S1` (byte-identita' a flag spento) NON e' qui: e' gia' sigillata da `_c1_semina_lam.py`")
P("    (`C1` PASS PIENO). Rifarla sarebbe contare due volte la stessa cosa.")
P("  - `S7` (giro di 120 passi) e' SOSPESO per decisione di Luca: la soglia della mitosi (`3pi`)")
P("    e' un numero tarato a posteriori nell'epoca 1, e va sostituita da una LEGGE DERIVATA.")
P("  - `S8` NON ESISTE nella scheda: la numerazione salta da `S7` a `S9`. Non ne invento uno.")
P("  - `S10` qui e' SOLO il passo ZERO. I passi 30/60/120 sono nel giro, quindi sospesi.")
P("  - `P-GONFIA` non e' qui: confronta la CRESCITA di `d0` nei 120 passi.")
P("  - le previsioni `P1`-`P5` vengono dal MANDATO, non le ho derivate io.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
sys.exit(0 if all(OK) else 1)
