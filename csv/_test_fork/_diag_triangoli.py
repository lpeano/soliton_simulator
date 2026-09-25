# -*- coding: utf-8 -*-
"""`2b` -- **CORSA DIAGNOSTICA SUI TRIANGOLI. NON E' IL TEST** *(mandato di Luca, 2026-09-25)*.

> *«CORSA DIAGNOSTICA (non è il test): scena `(ii)` `(b)`, campo maturo (dopo la cura 1),
> `300`-`800` passi, `2` semi. Misura sui TRIANGOLI: angolo SU(2) per arco, curvatura di Berry
> per triangolo, overlap di spin fra vicini, e se sono STRUTTURATI … o RUMORE.»*

**LA MITOSI RESTA QUELLA DI OGGI, CIOÈ MORTA** *(`SCALE-TW`: `max|tw| = 2.8991 π` contro una
soglia di `3π`, frazione raggiunta `0.000000`)*. **Va detto**, perché significa che in questa
corsa **il grafo non acquista nodi per mitosi**: quello che si misura è un grafo che evolve
**senza creazione**.

**PERCHÉ I TRIANGOLI E NON I CICLI DI `circolazione_topologica`** *(rilievo di Luca, e la misura
che lo sostiene)*: quei cicli sono **fondamentali di un albero**, **tappati a `256`**, di
lunghezza mediana **`19` archi**, e catturano **`41` triangoli su `1 697 590`** (`2.4e-05`).
**Una grandezza che dipende dall'ordine di visita non è una proprietà del grafo.**
**Il triangolo è il ciclo più corto possibile e non dipende da nessuna visita.**

**IL CAMPIONAMENTO È DICHIARATO:** i triangoli sono **milioni**; si estrae un campione di
`N_TRI` per istante, **con il generatore del test e non con quello della rete** *(per non
consumare `net.rng`: purezza pure-read)*.

**COSA DECIDE «STRUTTURATO» DA «RUMORE», e il nullo è scritto PRIMA** *(par.9)*:

```
overlap di spin fra vicini      nullo di direzioni CASUALI: <|<n_i|n_j>|^2> = 0.5
angolo chi fra vicini           nullo: media 90.000 gradi, std 39.171 gradi
curvatura di Berry per triangolo  nullo: media ~0, ampiezza ~ quella di tre overlap casuali
```

**E DUE PROVE DI STRUTTURA, non una:**
`(i)` **dipendenza massa/vuoto** — i triangoli dentro le regioni coerenti danno valori diversi da
quelli nel vuoto? `(ii)` **correlazione fra triangoli ADIACENTI** — due triangoli che condividono
un arco hanno curvature correlate? **Se entrambe sono nulle, è rumore.**

**➕ E SI MISURA ANCHE IL RAGGIO CIRCOSCRITTO `R` dei triangoli**, perché serve a valutare la
proposta `2c` *(creazione di faccia)*: `R = abc/(4K)` dalle **tre `d`**, senza `pos`.
**Il conto derivato, prima della misura:** per un triangolo equilatero `R = lato/sqrt(3)`, quindi
**`R >= LAM` richiede `lato >= sqrt(3) LAM = 1.7321 LAM`**.
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
FUORI = os.path.join(_QUI, "_diag_triangoli")
DEST = os.path.join(FUORI, "DIAG_triangoli.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEMI = [11, 12]
SEP = 4.0
PASSI = 300
ISTANTI = (0, 1, 60, 150, 300)
N_TRI = 4000        # il campione di triangoli per istante -- DICHIARATO

FIGLIO = r'''
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
import importlib.util as _iu
_sp = _iu.spec_from_file_location("sim_dt", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = True
S.SEMINA_MATURA = True          # IL CAMPO MATURO: e' la CURA 4
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
co = S.test["dati"]["coorti"]
rng = np.random.default_rng(1000 + SEME)      # IL GENERATORE DEL TEST, non `net.rng`

dentro0 = np.zeros(net.n, bool)
for k in range(3):
    dentro0[co["massa_%d" % k]] = True


def campiona_triangoli(net, quanti):
    """Campione di triangoli (a, b, c) con gli INDICI DEI TRE ARCHI. Solo topologia."""
    n = net.n
    ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
    # mappa (min,max) -> indice arco, e lista di adiacenza
    arco = {}
    adj = [[] for _ in range(n)]
    for e, (a, b) in enumerate(zip(ii, jj)):
        a = int(a); b = int(b)
        if a == b or a >= n or b >= n:
            continue
        arco[(min(a, b), max(a, b))] = e
        adj[a].append(b); adj[b].append(a)
    adj = [np.asarray(x, int) for x in adj]
    out = []
    tentativi = 0
    while len(out) < quanti and tentativi < quanti * 60:
        tentativi += 1
        a = int(rng.integers(0, n))
        if adj[a].size < 2:
            continue
        b, c = rng.choice(adj[a], size=2, replace=False)
        b = int(b); c = int(c)
        if b == c:
            continue
        k_bc = arco.get((min(b, c), max(b, c)))
        if k_bc is None:
            continue
        out.append((arco[(min(a, b), max(a, b))], arco[(min(a, c), max(a, c))], k_bc,
                    a, b, c))
    return out, tentativi


def misura(net, passo):
    o = dict(passo=int(passo), n=int(net.n), archi=int(len(net.d)))
    nb = getattr(net, "_nb", None)
    if nb is None or np.size(nb) == 0 or len(nb) < net.n:
        o["nb"] = False
        return o
    o["nb"] = True
    nb = np.asarray(nb, float)[:net.n]
    nb = nb / np.maximum(np.linalg.norm(nb, axis=1), 1e-30)[:, None]
    ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
    d = np.asarray(net.d, float)
    # --- ANGOLO SU(2) PER ARCO, e OVERLAP DI SPIN fra VICINI -------------------------------
    cosk = np.clip(np.sum(nb[ii] * nb[jj], axis=1), -1.0, 1.0)
    chi = np.arccos(cosk)
    o["chi_p50"] = float(np.median(chi)); o["chi_p95"] = float(np.percentile(chi, 95))
    o["chi_media_gradi"] = float(np.degrees(chi).mean())
    o["chi_std_gradi"] = float(np.degrees(chi).std())
    o["ovl2_media"] = float(np.mean((np.cos(chi / 2.0)) ** 2))   # |<n_i|n_j>|^2, nullo = 0.5
    # --- IL CAMPIONE DI TRIANGOLI ----------------------------------------------------------
    tri, tent = campiona_triangoli(net, N_TRI)
    o["tri_campionati"] = len(tri); o["tri_tentativi"] = tent
    if not tri:
        return o
    T = np.asarray([[t[0], t[1], t[2]] for t in tri], int)
    V = np.asarray([[t[3], t[4], t[5]] for t in tri], int)
    # CURVATURA DI BERRY del triangolo = fase dell'invariante di Bargmann
    #   <n_a|n_b><n_b|n_c><n_c|n_a>, costruito dagli SPINORI dei tre vertici.
    # Lo spinore si ricostruisce dal Bloch (fase globale irrilevante: l'invariante e' gauge-inv.)
    def spinore(v):
        th = np.arccos(np.clip(v[:, 2], -1.0, 1.0))
        ph = np.arctan2(v[:, 1], v[:, 0])
        return np.stack([np.cos(th / 2.0), np.exp(1j * ph) * np.sin(th / 2.0)], axis=1)
    sa = spinore(nb[V[:, 0]]); sb = spinore(nb[V[:, 1]]); sc = spinore(nb[V[:, 2]])
    ab = np.sum(np.conj(sa) * sb, axis=1)
    bc = np.sum(np.conj(sb) * sc, axis=1)
    ca = np.sum(np.conj(sc) * sa, axis=1)
    barg = ab * bc * ca
    berry = np.angle(barg)
    o["berry_media"] = float(berry.mean()); o["berry_std"] = float(berry.std())
    o["berry_abs_p50"] = float(np.median(np.abs(berry)))
    o["berry_abs_p95"] = float(np.percentile(np.abs(berry), 95))
    o["berry_abs_max"] = float(np.abs(berry).max())
    o["barg_mod_p50"] = float(np.median(np.abs(barg)))
    # --- (i) STRUTTURA: dentro le regioni contro il vuoto ---------------------------------
    dent = dentro0[:net.n] if len(dentro0) >= net.n else np.pad(dentro0, (0, net.n - len(dentro0)))
    tutti_dentro = dent[V].all(axis=1)
    tutti_fuori = (~dent[V]).all(axis=1)
    for et, m in (("dentro", tutti_dentro), ("vuoto", tutti_fuori)):
        if m.sum() >= 20:
            o["berry_abs_p50_%s" % et] = float(np.median(np.abs(berry[m])))
            o["chi_p50_%s" % et] = float(np.median(chi[T[m]].ravel()))
            o["conta_%s" % et] = int(m.sum())
        else:
            o["conta_%s" % et] = int(m.sum())
    # --- (ii) STRUTTURA: correlazione fra triangoli che CONDIVIDONO un arco ----------------
    da_arco = {}
    for k in range(len(T)):
        for e in T[k]:
            da_arco.setdefault(int(e), []).append(k)
    cop = [(v[0], v[1]) for v in da_arco.values() if len(v) >= 2]
    o["coppie_adiacenti"] = len(cop)
    if len(cop) >= 30:
        x = np.asarray([berry[a] for a, _ in cop], float)
        y = np.asarray([berry[b] for _, b in cop], float)
        sx, sy = x.std(), y.std()
        o["corr_adiacenti"] = float(np.mean((x - x.mean()) * (y - y.mean()) / (sx * sy))) \
            if sx > 0 and sy > 0 else float("nan")
        o["corr_nullo_3sigma"] = float(3.0 / np.sqrt(3.0 * len(cop)))
    # --- IL RAGGIO CIRCOSCRITTO, per valutare `2c` -----------------------------------------
    a_ = d[T[:, 0]]; b_ = d[T[:, 1]]; c_ = d[T[:, 2]]
    s = 0.5 * (a_ + b_ + c_)
    K2 = s * (s - a_) * (s - b_) * (s - c_)
    buoni = K2 > 0
    R = np.full(len(T), np.nan)
    R[buoni] = (a_[buoni] * b_[buoni] * c_[buoni]) / (4.0 * np.sqrt(K2[buoni]))
    Rv = R[np.isfinite(R)]
    LAM = float(S.LAM)
    if Rv.size:
        o["R_p05"] = float(np.percentile(Rv, 5)); o["R_p50"] = float(np.median(Rv))
        o["R_p95"] = float(np.percentile(Rv, 95)); o["R_max"] = float(Rv.max())
        o["R_su_LAM_p50"] = o["R_p50"] / LAM
        o["frazione_R_ge_LAM"] = float(np.mean(Rv >= LAM))
        o["frazione_degeneri"] = float(np.mean(~buoni))
        o["lato_p50_su_LAM"] = float(np.median(np.concatenate([a_, b_, c_])) / LAM)
    o["LAM"] = LAM
    return o


ris = []
for k in range(max(ISTANTI) + 1):
    if k:
        net.step()
    if k in ISTANTI:
        ris.append(misura(net, k))
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(ris))
print("OK %s  istanti %s  n finale %d" % (NOME, [r["passo"] for r in ris], net.n))
'''


def braccio(nome, seme):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nISTANTI = %r\nN_TRI = %d\n"
           % (RADICE, TMP, nome, seme, SEP, list(ISTANTI), N_TRI)) + FIGLIO
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.run([sys.executable, p], cwd=RADICE, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


LOG = []
for seme in SEMI:
    rr = braccio("s%d" % seme, seme)
    LOG.append("[s%d] rc=%d %s" % (seme, rr.returncode, (rr.stdout or "").strip()[-180:]))
    if rr.returncode:
        LOG.append((rr.stderr or "")[-1800:])

P_ = []


def P(s=""):
    P_.append(s)


P("=" * 118)
P("`2b` CORSA DIAGNOSTICA SUI TRIANGOLI -- **NON E' IL TEST**. Campo MATURO (CURA 4).")
P("=" * 118)
P()
P("LA MITOSI RESTA QUELLA DI OGGI, CIOE' MORTA (SCALE-TW: max|tw| = 2.8991 pi contro 3 pi,")
P("frazione raggiunta 0.000000). In questa corsa IL GRAFO NON ACQUISTA NODI PER MITOSI.")
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
for seme in SEMI:
    D[seme] = json.loads(io.open(os.path.join(TMP, "s%d.json" % seme), encoding="utf-8").read())

P("IL NULLO, SCRITTO PRIMA (par.9): direzioni di Bloch CASUALI danno")
P("   overlap |<n_i|n_j>|^2 = 0.5      chi: media 90.000 gradi, std 39.171 gradi")
P()
P("-" * 118)
P("%-6s %-6s %-9s %-9s %-11s %-11s %-11s %-11s %-11s"
  % ("seme", "passo", "n", "archi", "chi p50/pi", "ovl^2", "chi media", "chi std", "|berry| p50"))
P("-" * 118)
for seme in SEMI:
    for r in D[seme]:
        if not r.get("nb"):
            P("  %-4d %-6d  `_nb` ASSENTE" % (seme, r["passo"]))
            continue
        P("%-6d %-6d %-9d %-9d %-11.6f %-11.6f %-11.3f %-11.3f %-11.6f"
          % (seme, r["passo"], r["n"], r["archi"], r["chi_p50"] / np.pi, r["ovl2_media"],
             r["chi_media_gradi"], r["chi_std_gradi"], r.get("berry_abs_p50", float("nan"))))
P()
P("-" * 118)
P("STRUTTURATO O RUMORE? -- le DUE prove, e il nullo accanto")
P("-" * 118)
for seme in SEMI:
    for r in D[seme]:
        if not r.get("nb"):
            continue
        P("  seme %d, passo %d  (triangoli campionati %d su %d tentativi)"
          % (seme, r["passo"], r.get("tri_campionati", 0), r.get("tri_tentativi", 0)))
        P("     overlap^2 misurato %.6f   contro il nullo 0.5   -> scarto %+.6f"
          % (r["ovl2_media"], r["ovl2_media"] - 0.5))
        P("     chi: media %.3f std %.3f   contro il nullo 90.000 / 39.171"
          % (r["chi_media_gradi"], r["chi_std_gradi"]))
        if "berry_abs_p50_dentro" in r and "berry_abs_p50_vuoto" in r:
            P("     (i)  DENTRO le regioni |berry| p50 = %.6f (%d tri)   VUOTO %.6f (%d tri)"
              % (r["berry_abs_p50_dentro"], r.get("conta_dentro", 0),
                 r["berry_abs_p50_vuoto"], r.get("conta_vuoto", 0)))
            _rr = (r["berry_abs_p50_dentro"] / r["berry_abs_p50_vuoto"]
                   if r["berry_abs_p50_vuoto"] else float("inf"))
            P("          rapporto dentro/vuoto = %.4f   (1.0 = nessuna dipendenza)" % _rr)
        else:
            P("     (i)  NON MISURABILE: triangoli tutti-dentro %d, tutti-fuori %d (serve >= 20)"
              % (r.get("conta_dentro", 0), r.get("conta_vuoto", 0)))
        if "corr_adiacenti" in r:
            P("     (ii) correlazione fra triangoli che condividono un arco: %+.6f"
              % r["corr_adiacenti"])
            P("          su %d coppie; il nullo a 3 sigma vale %.6f -> %s"
              % (r["coppie_adiacenti"], r["corr_nullo_3sigma"],
                 "OLTRE il nullo" if abs(r["corr_adiacenti"]) > r["corr_nullo_3sigma"]
                 else "DENTRO il nullo"))
        else:
            P("     (ii) NON MISURABILE: coppie adiacenti nel campione = %d (servono >= 30)"
              % r.get("coppie_adiacenti", 0))
        P()
P("-" * 118)
P("IL RAGGIO CIRCOSCRITTO `R`, per valutare la proposta `2c` (creazione di faccia)")
P("-" * 118)
P("  Il conto DERIVATO, scritto prima: equilatero -> R = lato/sqrt(3), quindi")
P("  R >= LAM  <=>  lato >= sqrt(3) LAM = 1.7321 LAM.")
P()
P("  %-6s %-6s %-12s %-12s %-12s %-14s %-14s" % ("seme", "passo", "R/LAM p05", "R/LAM p50",
                                                 "R/LAM p95", "frazione >= LAM", "degeneri"))
for seme in SEMI:
    for r in D[seme]:
        if "R_p50" not in r:
            continue
        L = r["LAM"]
        P("  %-6d %-6d %-12.4f %-12.4f %-12.4f %-14.6f %-14.6f"
          % (seme, r["passo"], r["R_p05"] / L, r["R_p50"] / L, r["R_p95"] / L,
             r["frazione_R_ge_LAM"], r["frazione_degeneri"]))
P()
P("COSA QUESTA CORSA NON DICE, e va detto:")
P("  - NON E' IL TEST: e' una diagnostica. Nessun criterio di promozione si legge qui.")
P("  - DUE SEMI: par.0-ter `P3` chiede >= 4 per una barra fra semi. Con 2, t(0.025,1) = 12.706.")
P("  - LA MITOSI E' MORTA in questa corsa: il grafo non acquista nodi per mitosi.")
P("  - il campione di triangoli e' %d per istante, estratto col generatore DEL TEST: `net.rng`" % N_TRI)
P("    NON viene consumato (purezza pure-read).")
P("  - la curvatura di Berry e' ricostruita dai BLOCH; la fase globale non conta perche'")
P("    l'invariante di Bargmann e' gauge-invariante -- ma NON e' `berry_spin` di")
P("    `circolazione_topologica`, che gira sui suoi cicli lunghi.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
