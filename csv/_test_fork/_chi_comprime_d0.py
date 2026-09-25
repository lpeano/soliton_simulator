# -*- coding: utf-8 -*-
"""**CHI COMPRIME `d0`** — bilancio PER SCRITTORE, e uniforme o differenziale? *(Luca, 2026-09-25)*

> *«Nella rimisura `med d0` scende da `1.884` a `1.200` (campo maturo) e a `0.800 = LAM` esatto
> (campo spento). `P-GONFIA` come scritto non ha oggetto: registralo. Misura, con lo strumento del
> bilancio di `d0` PER SCRITTORE: quanto contribuisce ogni scrittore alla contrazione; la
> contrazione è UNIFORME o DIFFERENZIALE; nel braccio spento che frazione di archi sta a
> `d0 == LAM` esatto. Solo misura, nessuna cura.»*

**COME, senza toccare il simulatore:** si accende **`TRACCIA_D0`** *(che è il meccanismo già
cablato: `_traccia_d0` è chiamata da **20 siti**, `S01`-`S12` gli scrittori e `P1`-`P7` i
pavimenti)* **e si AVVOLGE `_traccia_d0`** per sommare, a ogni chiamata, **`sum(d0) − sum(prima)`
su TUTTI gli archi**. `_traccia_d0` è dichiarata *«PURE-READ sulla fisica»*: avvolgerla non
cambia nulla.

**⚠ PERCHÉ NON BASTA IL LIVELLO (b) DEL TRACCIATORE:** quello somma **solo sugli archi di
`TRACCIA_D0_NODI`** *(cinque nodi)*. **Per un bilancio GLOBALE serve la somma su tutti gli archi**,
e la si calcola nell'involucro.

**LA DOMANDA CHE DECIDE, e il criterio è scritto prima:**

```
UNIFORME       tutte le classi di arco si contraggono nella stessa proporzione
               -> NON E' GRAVITA': e' una scala che cambia
DIFFERENZIALE  gli archi FRA MASSE si contraggono PIU' degli altri
               -> e' la prima cosa da guardare per la PROVA 1 (due masse si avvicinano?)
```

**LE CLASSI DI ARCO, dai nodi:** `dentro-i` *(entrambi nella stessa regione)*, `fra-masse`
*(in due regioni diverse)*, `massa-vuoto`, `vuoto-vuoto`. **Calcolate al passo zero e tenute
fisse**, perché se le si ricalcolasse a ogni passo si mescolerebbe la contrazione col
rimescolamento delle coorti.

**Solo misura. Nessuna cura.**
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
FUORI = os.path.join(_QUI, "_chi_comprime_d0")
DEST = os.path.join(FUORI, "CHI_COMPRIME_d0.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEMI = [11, 12]
SEP = 4.0
PASSI = 120

FIGLIO = r'''
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import importlib.util as _iu
import _passo
_sp = _iu.spec_from_file_location("sim_cd", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = True
S.SEMINA_MATURA = bool(FLAG)
S.SCALA_MIN_PASSO = True        # come il driver
S.SCALA_MIN = False
S.TRACCIA_D0 = True             # il meccanismo GIA' cablato: 20 siti

# --- L'INVOLUCRO SU `_traccia_d0`: il BILANCIO GLOBALE per SITO. Pure-read su pure-read. ---
BIL = {}
_orig = S.Rete._traccia_d0


def _wrap(self, sito, prima, pavimento=None):
    _p = np.asarray(prima, float)
    _d = np.asarray(self.d0, float)
    v = BIL.setdefault(sito, dict(giri=0, delta=0.0, delta_pos=0.0, delta_neg=0.0,
                                  lung_prima=0, lung_dopo=0, concat=0))
    v["giri"] += 1
    if _p.size == _d.size:
        _dd = _d - _p
        v["delta"] += float(_dd.sum())
        v["delta_pos"] += float(_dd[_dd > 0].sum())
        v["delta_neg"] += float(_dd[_dd < 0].sum())
    else:
        # I SITI CHE CONCATENANO cambiano la LUNGHEZZA: li' il delta elemento-per-elemento non
        # esiste, e si registra il cambio di lunghezza -- come fa il tracciatore vero.
        v["concat"] += 1
        v["lung_prima"] = int(_p.size); v["lung_dopo"] = int(_d.size)
    return _orig(self, sito, prima, pavimento)


S.Rete._traccia_d0 = _wrap

# ❌❌ IL BILANCIO NON CHIUDEVA, ED ERA UNA MIA OMISSIONE, NON UN RISULTATO.
#   `_smp_chiudi` -- IL FRENO su `d0` -- riscrive `d0` SENZA passare da `_traccia_d0`, e
#   **sta scritto nel docstring di `_g4_prova`**: "`_smp_chiudi` riscrive `d0` SENZA traccia:
#   si prende da `_smorza`". Avevo letto quello strumento per sapere QUALE meccanismo usare,
#   **e non ho letto la riga che diceva che uno scrittore manca.**
#   MISURATO nella prima corsa: residuo `+6.09e5` (maturo) e `+8.33e6` (spento), dello
#   stesso ordine della somma degli scrittori. **Non era uno scrittore SCONOSCIUTO: era
#   quello che l'altro strumento NOMINA.**
_orig_sm = S.Rete._smorza


def _wrap_sm(self, prima, dx, quale):
    _fuori = _orig_sm(self, prima, dx, quale)
    _p = np.asarray(prima, float)
    _f = np.asarray(_fuori, float)
    _dx = np.asarray(dx, float)
    v = BIL.setdefault('FRENO_' + str(quale), dict(giri=0, delta=0.0, delta_pos=0.0,
                                                   delta_neg=0.0, lung_prima=0,
                                                   lung_dopo=0, concat=0))
    v['giri'] += 1
    if _p.size == _f.size == _dx.size:
        # il FRENO cambia l'INCREMENTO: il suo contributo e' `smorzato - grezzo`
        _dd = _f - _dx
        v['delta'] += float(_dd.sum())
        v['delta_pos'] += float(_dd[_dd > 0].sum())
        v['delta_neg'] += float(_dd[_dd < 0].sum())
    else:
        v['concat'] += 1
        v['lung_prima'] = int(_p.size); v['lung_dopo'] = int(_f.size)
    return _fuori


S.Rete._smorza = _wrap_sm

S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
co = S.test["dati"]["coorti"]
LAM = float(S.LAM)

# --- LE CLASSI DI ARCO, calcolate AL PASSO ZERO e TENUTE FISSE ------------------------------
n0 = int(net.n)
regione = np.full(n0, -1, int)          # -1 = vuoto
for k in range(3):
    idx = co["massa_%d" % k]
    regione[idx[idx < n0]] = k
ii0 = np.asarray(net.i, int).copy(); jj0 = np.asarray(net.j, int).copy()
ok = (ii0 < n0) & (jj0 < n0)
ri, rj = regione[ii0[ok]], regione[jj0[ok]]
CLASSI = {
    "dentro-massa": (ri >= 0) & (rj >= 0) & (ri == rj),
    "fra-masse": (ri >= 0) & (rj >= 0) & (ri != rj),
    "massa-vuoto": ((ri >= 0) & (rj < 0)) | ((ri < 0) & (rj >= 0)),
    "vuoto-vuoto": (ri < 0) & (rj < 0),
}
IDX0 = np.where(ok)[0]
d0_ini = np.asarray(net.d0, float).copy()

# ❗ `fra-masse` HA ZERO ARCHI, E NON E' UN DIFETTO: E' LA SCENA.
#   Il varco fra le superfici delle regioni e' `R_CONN` PER COSTRUZIONE, quindi **le regioni
#   non si allacciano direttamente**. **La domanda "la contrazione avvicina le masse?" NON
#   si misura sugli archi diretti: non ce ne sono.**
#   SI MISURA IL PONTE fra i nuclei, in DUE modi:
#     (a) i passi in ARCHI (cammino minimo sul grafo);
#     (b) LA SOMMA DEI `d0` lungo quel cammino -- la lunghezza metrica del ponte.
#   ⚠ E' (b) che conta per la PROVA 1: se il grafo si contrae UNIFORMEMENTE cala come
#     tutto il resto; se le masse si AVVICINANO, cala DI PIU'. Il nullo sono gli archi
#     vuoto-vuoto.
import collections


def _nuclei(net, co, n):
    # il nucleo di ogni regione: il nodo della coorte col GRADO piu' alto (il piu' interno)
    grado = np.zeros(n, int)
    ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
    m = (ii < n) & (jj < n)
    np.add.at(grado, ii[m], 1); np.add.at(grado, jj[m], 1)
    out = []
    for k in range(3):
        idx = co['massa_%d' % k]
        idx = idx[idx < n]
        out.append(int(idx[np.argmax(grado[idx])]) if idx.size else -1)
    return out


def _ponte(net, a, b, n):
    # (passi in archi, somma dei `d0`) lungo il cammino minimo. BFS, solo topologia.
    if a < 0 or b < 0 or a >= n or b >= n:
        return None, None
    ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
    d0 = np.asarray(net.d0, float)
    adj = collections.defaultdict(list)
    for e, (x, y) in enumerate(zip(ii, jj)):
        x = int(x); y = int(y)
        if x == y or x >= n or y >= n or e >= d0.size:
            continue
        adj[x].append((y, e)); adj[y].append((x, e))
    prev = {a: (None, None)}
    q = collections.deque([a])
    while q:
        u = q.popleft()
        if u == b:
            break
        for v, e in adj[u]:
            if v not in prev:
                prev[v] = (u, e)
                q.append(v)
    if b not in prev:
        return None, None
    passi, lung, x = 0, 0.0, b
    while prev[x][0] is not None:
        u, e = prev[x]
        passi += 1
        lung += float(d0[e])
        x = u
    return passi, lung


NUC = _nuclei(net, co, n0)
# ⚠ il PONTE INIZIALE si registra DOPO che `o` esiste (sotto): qui `o` non c'e' ancora, e
#   la prima stesura moriva con `NameError: name 'o' is not defined` su tutti e quattro i
#   bracci. Un ordine sbagliato di due righe, e il guardiano era lo schianto.

o = dict(FLAG=bool(FLAG), SEME=SEME, n0=n0, archi0=int(len(net.d)), LAM=LAM, PASSI=int(PASSI),
         classi={k: int(v.sum()) for k, v in CLASSI.items()},
         d0_med_ini=float(np.median(d0_ini)))
o['nuclei'] = NUC
for _a, _b in ((0, 1), (0, 2), (1, 2)):
    pa, lu = _ponte(net, NUC[_a], NUC[_b], n0)
    o['ponte_ini_%d%d_passi' % (_a, _b)] = pa
    o['ponte_ini_%d%d_lung' % (_a, _b)] = lu
for k, m in CLASSI.items():
    if m.sum() >= 10:
        o["ini_" + k] = float(np.median(d0_ini[IDX0[m]]))

for _ in range(PASSI):
    _passo.passo_pieno(S, net)

d0_fin = np.asarray(net.d0, float)
o["d0_med_fin"] = float(np.median(d0_fin))
o["archi_fin"] = int(len(net.d))
# gli archi originali sono ancora ai loro indici? la mitosi RIMUOVE l'arco diviso, quindi NO:
# si confronta solo se la lunghezza e' compatibile, e SI DICHIARA.
o["confrontabile"] = bool(d0_fin.size >= IDX0.max() + 1)
if o["confrontabile"]:
    for k, m in CLASSI.items():
        if m.sum() >= 10:
            o["fin_" + k] = float(np.median(d0_fin[IDX0[m]]))
# la frazione a `d0 == LAM` ESATTO
# il PONTE a fine corsa: la stessa misura, per la PROVA 1
for _a, _b in ((0, 1), (0, 2), (1, 2)):
    pa, lu = _ponte(net, NUC[_a], NUC[_b], int(net.n))
    o['ponte_fin_%d%d_passi' % (_a, _b)] = pa
    o['ponte_fin_%d%d_lung' % (_a, _b)] = lu
o["fraz_d0_a_LAM"] = float(np.mean(d0_fin == LAM))
o["fraz_d0_sotto_1p01LAM"] = float(np.mean(d0_fin <= 1.01 * LAM))
o["d0_min_fin"] = float(d0_fin.min())
o["bilancio"] = BIL
o["somma_scrittori"] = float(sum(v["delta"] for k, v in BIL.items() if k.startswith("S")))
o["somma_pavimenti"] = float(sum(v["delta"] for k, v in BIL.items() if k.startswith("P")))
# ❌❌ IL BILANCIO MESCOLAVA `d` E `d0`, ED E' ESATTAMENTE L'ERRORE DI `U2`.
#   `FRENO_d_passo` frena **`d`**, non `d0`: sommarlo al bilancio di `d0` e' un errore di
#   CATEGORIA. MISURATO: il residuo valeva `-1.101e4` (maturo) e `-1.091e4` (spento) --
#   **quasi identici**, e quasi esattamente `-FRENO_d_passo` (`+1.103e4`, `+1.096e4`).
#   **Un residuo COSTANTE fra due bracci diversissimi era il segno che non veniva dalla
#   fisica: veniva da un termine che non c'entrava.**
o["somma_freno_d0"] = float(sum(v["delta"] for k, v in BIL.items()
                               if k.startswith("FRENO_d0")))
o["somma_freno_d"] = float(sum(v["delta"] for k, v in BIL.items()
                              if k.startswith("FRENO_") and not k.startswith("FRENO_d0")))
o["somma_freno"] = o["somma_freno_d0"]      # nel bilancio di `d0` entra SOLO quello di `d0`
o["crescita_vera"] = float(d0_fin.sum() - d0_ini.sum()) if o["confrontabile"] else float("nan")
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  med d0 %.6f -> %.6f   archi %d -> %d"
      % (NOME, o["d0_med_ini"], o["d0_med_fin"], o["archi0"], o["archi_fin"]))
'''


def braccio(nome, seme, flag):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nFLAG = %r\nPASSI = %d\n"
           % (RADICE, TMP, nome, seme, SEP, flag, PASSI)) + FIGLIO
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


BR = [("mat_s%d" % s, s, True) for s in SEMI] + [("spe_s%d" % s, s, False) for s in SEMI]
# `--rileggi` rilegge i JSON gia' sul disco invece di rigirare la simulazione. Serve
#   quando si corregge SOLO LA LETTURA: rigirare una simulazione per cambiare una formula
#   di stampa **bruciarebbe tempo e non cambierebbe un dato**. E se i JSON non ci sono,
#   RIFIUTA invece di girare a meta'.
RILEGGI = ("--rileggi" in sys.argv)
LOG = []
if RILEGGI:
    for n, _s, _f in BR:
        _p = os.path.join(TMP, n + ".json")
        if not os.path.isfile(_p):
            raise SystemExit("[rileggi] manca %s: non rileggo a meta'." % _p)
        LOG.append("[%s] RILETTO dal json (nessuna simulazione rigirata)" % n)
else:
    proc = {n: braccio(n, s, f) for n, s, f in BR}
    for n, pr in proc.items():
        so, se = pr.communicate()
        LOG.append("[%s] rc=%d %s" % (n, pr.returncode,
                                      (so or b"").decode("utf-8", "replace").strip()[-140:]))
        if pr.returncode:
            LOG.append((se or b"").decode("utf-8", "replace")[-1500:])

P_ = []


def P(x=""):
    P_.append(x)


P("=" * 118)
P("**CHI COMPRIME `d0`** — bilancio PER SCRITTORE, e uniforme o differenziale?")
P("=" * 118)
P()
P("  " + _passo.descrivi())
P("  scena (ii) (b), %d passi, %d semi, campo MATURO e SPENTO, freno ON come il driver."
  % (PASSI, len(SEMI)))
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
    d = json.loads(io.open(os.path.join(TMP, n + ".json"), encoding="utf-8").read())
    # i json della corsa PRECEDENTE non hanno i campi separati: si ricavano dal bilancio,
    # che c'e' per intero. Cosi' `--rileggi` funziona anche su di essi, e SI DICHIARA.
    B = d.get("bilancio", {})
    if "somma_freno_d0" not in d:
        d["somma_freno_d0"] = float(sum(v["delta"] for k, v in B.items()
                                       if k.startswith("FRENO_d0")))
        d["somma_freno_d"] = float(sum(v["delta"] for k, v in B.items()
                                      if k.startswith("FRENO_")
                                      and not k.startswith("FRENO_d0")))
        d["somma_freno"] = d["somma_freno_d0"]
        d["_ricavato_da_bilancio"] = True
    return d


D = {n: leggi(n) for n, _, _ in BR}
MAT = [D["mat_s%d" % s] for s in SEMI]
SPE = [D["spe_s%d" % s] for s in SEMI]


def mm(lista, campo):
    v = [x[campo] for x in lista if campo in x and x[campo] == x[campo]]
    return (float(np.mean(v)), float(np.max(v) - np.min(v))) if v else (float("nan"), float("nan"))


P("-" * 118)
P("1. LA CONTRAZIONE, e `P-GONFIA` NON HA OGGETTO")
P("-" * 118)
for et, L in (("MATURO", MAT), ("SPENTO", SPE)):
    a, _ = mm(L, "d0_med_ini")
    b, sb = mm(L, "d0_med_fin")
    P("  %-8s med d0  %.6f -> %.6f  (spread fra semi %.1e)   variazione %+.2f %%"
      % (et, a, b, sb, 100.0 * (b - a) / a if a else float("nan")))
P("  `P-GONFIA` prevede una CRESCITA e una soglia «meno della meta' di +47.28 %».")
P("  -> **NELLA SCENA (ii) `d0` NON CRESCE: SI CONTRAE. IL CRITERIO NON HA UN OGGETTO.**")
P("     Non e' «passato»: misura una crescita che non c'e'. **REGISTRATO.**")
P()
P("-" * 118)
P("2. IL BILANCIO PER SCRITTORE (somma su TUTTI gli archi, cumulativa su %d passi)" % PASSI)
P("-" * 118)
for et, L in (("MATURO", MAT), ("SPENTO", SPE)):
    P("  braccio %s:" % et)
    siti = sorted({k for x in L for k in x["bilancio"]})
    P("    %-18s %-8s %-14s %-14s %-14s %-8s"
      % ("sito", "giri", "delta TOTALE", "solo POSITIVI", "solo NEGATIVI", "concat"))
    for s in siti:
        dl = [x["bilancio"][s]["delta"] for x in L if s in x["bilancio"]]
        dp = [x["bilancio"][s]["delta_pos"] for x in L if s in x["bilancio"]]
        dn = [x["bilancio"][s]["delta_neg"] for x in L if s in x["bilancio"]]
        gi = [x["bilancio"][s]["giri"] for x in L if s in x["bilancio"]]
        cc = [x["bilancio"][s]["concat"] for x in L if s in x["bilancio"]]
        P("    %-18s %-8.0f %-+14.6e %-+14.6e %-+14.6e %-8.0f"
          % (s, np.mean(gi), np.mean(dl), np.mean(dp), np.mean(dn), np.mean(cc)))
    ss, _ = mm(L, "somma_scrittori")
    sp, _ = mm(L, "somma_pavimenti")
    sf, _ = mm(L, "somma_freno")
    cv, _ = mm(L, "crescita_vera")
    P("    SOMMA scrittori (`S*`) = %+.6e      SOMMA pavimenti (`P*`) = %+.6e" % (ss, sp))
    sfd, _ = mm(L, "somma_freno_d")
    P("    SOMMA FRENO su `d0` (`_smorza`, che NON passa da `_traccia_d0`) = %+.6e" % sf)
    P("    (e il freno su `d` vale %+.6e: NON entra nel bilancio di `d0` -- sommarlo era" % sfd)
    P("     un errore di CATEGORIA, lo stesso di `U2`, e il residuo COSTANTE fra i due")
    P("     bracci lo ha denunciato.)")
    P("    CRESCITA VERA di `sum(d0)` = %+.6e" % cv)
    _res = cv - (ss + sp + sf)
    P("    RESIDUO = crescita vera - (scrittori + pavimenti + FRENO) = %+.6e" % _res)
    _rel = abs(_res) / max(abs(cv), 1e-300)
    P("    RESIDUO RELATIVO alla crescita vera = %.3e" % _rel)
    P("    -> il bilancio %s"
      % ("CHIUDE (residuo relativo < 1e-3)" if _rel < 1e-3
         else ("chiude entro l'1 %%" if _rel < 1e-2
               else "NON CHIUDE: c'e' uno scrittore NON TRACCIATO, ed e' il risultato")))
    P()
P("-" * 118)
P("3. UNIFORME O DIFFERENZIALE? — il criterio era scritto prima")
P("-" * 118)
for et, L in (("MATURO", MAT), ("SPENTO", SPE)):
    P("  braccio %s   (confrontabile: %s)"
      % (et, all(x.get("confrontabile") for x in L)))
    P("    %-16s %-9s %-12s %-12s %-12s" % ("classe", "archi", "med ini", "med fin", "variazione"))
    for k in ("dentro-massa", "fra-masse", "massa-vuoto", "vuoto-vuoto"):
        na = np.mean([x["classi"].get(k, 0) for x in L])
        a, _ = mm(L, "ini_" + k)
        b, _ = mm(L, "fin_" + k)
        if a != a or b != b:
            P("    %-16s %-9.0f  NON MISURATO (meno di 10 archi, o non confrontabile)" % (k, na))
            continue
        P("    %-16s %-9.0f %-12.6f %-12.6f %+-12.2f %%" % (k, na, a, b, 100.0 * (b - a) / a))
    P()
_fr = {}
for et, L in (("MATURO", MAT), ("SPENTO", SPE)):
    vv = [x for x in L]
    d_ = {}
    for k in ("dentro-massa", "fra-masse", "massa-vuoto", "vuoto-vuoto"):
        a, _ = mm(vv, "ini_" + k)
        b, _ = mm(vv, "fin_" + k)
        if a == a and b == b and a:
            d_[k] = 100.0 * (b - a) / a
    _fr[et] = d_
for et, d_ in _fr.items():
    if len(d_) >= 2:
        sp = max(d_.values()) - min(d_.values())
        P("  %-8s escursione fra classi = %.2f punti percentuali" % (et, sp))
        peg = min(d_, key=lambda z: d_[z])
        P("           la classe che si contrae PIU' e': **%s** (%.2f %%)" % (peg, d_[peg]))
        if abs(sp) < 1.0:
            P("           -> **UNIFORME entro 1 punto: NON E' GRAVITA', e' una scala che cambia.**")
        elif peg == "fra-masse":
            P("           -> ** DIFFERENZIALE, E NELLA DIREZIONE DELLA PROVA 1: gli archi FRA")
            P("              MASSE si contraggono PIU' degli altri. E' la prima cosa da guardare. **")
        else:
            P("           -> DIFFERENZIALE, ma la classe che si contrae piu' NON e' `fra-masse`:")
            P("              non e' l'avvicinamento fra masse. Va detto cosi'.")
P()
P("-" * 118)
P("3-bis. LA PROVA 1: LE MASSE SI AVVICINANO? -- e `fra-masse` non ha archi PER COSTRUZIONE")
P("-" * 118)
P("  Il varco fra le superfici e' `R_CONN` PER COSTRUZIONE della scena, quindi LE REGIONI")
P("  NON SI ALLACCIANO DIRETTAMENTE: `fra-masse` ha ZERO archi, e NON e' un difetto.")
P("  Si misura IL PONTE fra i nuclei: passi in ARCHI e SOMMA dei `d0` lungo il cammino minimo.")
P("  \u26a0 E' la somma dei `d0` che conta per la PROVA 1: se il grafo si contrae UNIFORMEMENTE")
P("     cala come tutto il resto; se le masse si AVVICINANO, cala DI PIU'. Il nullo sono gli")
P("     archi vuoto-vuoto.")
P()
for et, L in (("MATURO", MAT), ("SPENTO", SPE)):
    P("  braccio %s" % et)
    P("    %-8s %-22s %-24s %-14s" % ("coppia", "passi (ini -> fin)",
                                      "somma d0 (ini -> fin)", "variazione"))
    _var = []
    for a_, b_ in ((0, 1), (0, 2), (1, 2)):
        pi_, _ = mm(L, "ponte_ini_%d%d_passi" % (a_, b_))
        pf_, _ = mm(L, "ponte_fin_%d%d_passi" % (a_, b_))
        li_, _ = mm(L, "ponte_ini_%d%d_lung" % (a_, b_))
        lf_, _ = mm(L, "ponte_fin_%d%d_lung" % (a_, b_))
        if li_ != li_ or lf_ != lf_:
            P("    %-8s NON MISURATO (nuclei non connessi)" % ("%d-%d" % (a_, b_)))
            continue
        v_ = 100.0 * (lf_ - li_) / li_ if li_ else float("nan")
        _var.append(v_)
        P("    %-8s %-22s %-24s %+-14.2f %%"
          % ("%d-%d" % (a_, b_), "%.1f -> %.1f" % (pi_, pf_),
             "%.4f -> %.4f" % (li_, lf_), v_))
    if _var:
        _mv = float(np.mean(_var))
        _vv, _ = mm(L, "ini_vuoto-vuoto")
        _vf, _ = mm(L, "fin_vuoto-vuoto")
        _base = 100.0 * (_vf - _vv) / _vv if _vv else float("nan")
        P("    media della variazione del PONTE = %+.2f %%   contro %+.2f %% del vuoto-vuoto"
          % (_mv, _base))
        # ⚠ E IL VERDETTO VA LETTO COL PAVIMENTO, senno' si legge la SATURAZIONE come
        #   gravita'. Se la mediana del vuoto e' ARRIVATA a `LAM`, tutto sta collassando
        #   sul pavimento, e un ponte che parte PIU' LUNGO cala di PIU' in percentuale
        #   **solo perche' ha piu' strada da fare**: e' REGRESSIONE VERSO IL PAVIMENTO.
        _lam, _ = mm(L, "LAM")
        _al_pav = bool(_vf <= 1.001 * _lam)
        _pa_ini = li_ / max(pi_, 1) if pi_ else float("nan")
        P("    il vuoto finisce a %.6f (LAM = %.6f): %s"
          % (_vf, _lam, "AL PAVIMENTO" if _al_pav else "sopra il pavimento"))
        _fr, _ = mm(L, "fraz_d0_a_LAM")
        P("    frazione di archi a `LAM` esatto = %.6f" % _fr)
        if _al_pav:
            P("    -> ⛔ **NON SI LEGGE COME GRAVITA': il vuoto E' AL PAVIMENTO.** Il ponte")
            P("       partiva PIU' LUNGO della mediana, quindi cala di piu' in percentuale")
            P("       **solo perche' ha piu' strada da fare fino allo stesso pavimento**.")
            P("       E' REGRESSIONE VERSO IL PAVIMENTO, non avvicinamento.")
        elif _mv < _base - 1.0:
            P("    -> ** IL PONTE SI ACCORCIA PIU' DEL VUOTO: LE MASSE SI AVVICINANO. **")
        elif _mv > _base + 1.0:
            P("    -> il ponte si accorcia MENO del vuoto: si ALLONTANANO relativamente.")
        else:
            P("    -> il ponte segue il vuoto entro 1 punto: CONTRAZIONE UNIFORME, NON gravita'.")
    P()
P("-" * 118)
P("4. IL PAVIMENTO CHE MORDE — frazione di archi a `d0 == LAM` ESATTO, a fine corsa")
P("-" * 118)
for et, L in (("MATURO", MAT), ("SPENTO", SPE)):
    a, sa = mm(L, "fraz_d0_a_LAM")
    b, _ = mm(L, "fraz_d0_sotto_1p01LAM")
    mn, _ = mm(L, "d0_min_fin")
    P("  %-8s a `LAM` ESATTO: %.6f (spread %.1e)    entro 1.01 LAM: %.6f    min(d0) = %.9f"
      % (et, a, sa, b, mn))
P("  (`d0 == LAM` esatto e' il segno che il PAVIMENTO ha MORSO, non che la fisica si e'")
P("   fermata li': un'uguaglianza esatta in floating point viene da un `maximum`.)")
P()
P("COSA QUESTO NON DICE:")
P("  - DUE SEMI: par.0-ter `P3` chiede >= 4 per una barra. Con 2, t(0.025,1) = 12.706.")
P("  - le CLASSI sono calcolate al passo ZERO e tenute FISSE: se le si ricalcolasse a ogni")
P("    passo si mescolerebbe la contrazione col rimescolamento delle coorti. **Ma la MITOSI")
P("    RIMUOVE l'arco diviso**, quindi gli indici possono slittare: la colonna «confrontabile»")
P("    dice se il confronto e' stato fatto, e dove non lo e' si legge NON MISURATO.")
P("  - SOLO MISURA. Nessuna cura, per mandato.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
