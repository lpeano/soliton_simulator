# -*- coding: utf-8 -*-
"""**DOVE STA `omega` ESTREMO** — e la traiettoria nel braccio SPENTO, che mancava.

> **Rilievo di Luca, 2026-09-25:** *«`max|omega|` cresce `~×1000` fra passo `1` e `300` e lo
> spread fra semi supera la mediana. **Il criterio «quasi monotona» era troppo largo: una
> crescita non monotona può essere illimitata.** Prima dei run lunghi, a basso costo:
> LOCALIZZA i nodi con `|omega|` estremo (top `0.1 %`): `eta`/`ramp` (appena nati?), inerzia al
> pavimento `max(_rho_sorgente, 1e-6)`? massa o vuoto? — e la stessa traiettoria nel braccio
> SPENTO, come nullo (era nel criterio e non è riportata).»*

**HA RAGIONE SUL CRITERIO, e lo scrivo prima dei numeri:** avevo chiesto *«crescita in `>= 95 %`
dei passi»*, e con `0.023`-`0.143` ho concluso *«non diverge»*. **Ma una successione può crescere
di `×1000` salendo a scatti e scendendo spesso**: la monotonia è una condizione **sufficiente**
per la divergenza, **non necessaria**. **Il criterio giusto guarda il LIVELLO, non la forma.**

**IL NULLO È IL BRACCIO SPENTO**, e mancava: se `max|omega|` cresce `×1000` **anche a campo
spento**, la crescita **non viene dalla `CURA 4`**.

**COSA SI MISURA sul top `0.1 %` per `|omega|`**, e tutto esiste già:

```
eta, ramp                           appena nati?
_rho_sorgente()                     e quanti sono AL PAVIMENTO `1e-6` (l'inerzia bloccata)
regione                             massa o vuoto?
grado, d mediano degli archi        isolati? con archi corti?
```

**Costo: basso.** `120` passi, `2` semi, **due bracci** — non `300` e non `4`.
**Solo misura.**
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
FUORI = os.path.join(_QUI, "_dove_sta_omega")
DEST = os.path.join(FUORI, "DOVE_STA_OMEGA.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEMI = [11, 12]
SEP = 4.0
PASSI = 120
ISTANTI = (1, 20, 60, 120)

FIGLIO = r'''
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import importlib.util as _iu
import _passo
_sp = _iu.spec_from_file_location("sim_do", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = True
S.SEMINA_MATURA = bool(FLAG)
S.SCALA_MIN_PASSO = True
S.SCALA_MIN = False
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
co = S.test["dati"]["coorti"]
n0 = int(net.n)
dentro0 = np.zeros(n0, bool)
for k in range(3):
    idx = co["massa_%d" % k]
    dentro0[idx[idx < n0]] = True

PAV = 1e-6          # il pavimento dell'inerzia, letto dal par.9: max(_rho_sorgente(), 1e-6)
ris = []
trai = []
for k in range(PASSI + 1):
    if k:
        _passo.passo_pieno(S, net)
    om = np.linalg.norm(np.asarray(net.omega_s, float), axis=1) if np.size(net.omega_s) \
        else np.zeros(1)
    trai.append((k, float(om.max()) if om.size else float("nan"),
                 float(np.median(om)) if om.size else float("nan"),
                 float(np.max(np.abs(net.phivel))) if np.size(net.phivel) else float("nan"),
                 int(net.n)))
    if k not in ISTANTI or not om.size:
        continue
    n = int(net.n)
    om = om[:n]
    q = max(1, int(np.ceil(0.001 * n)))          # il TOP 0.1 %
    top = np.argsort(om)[::-1][:q]
    rho = np.asarray(net._rho_sorgente(), float)
    rho = rho[:n] if rho.size >= n else np.pad(rho, (0, n - rho.size))
    inerzia = np.maximum(rho, PAV)
    _tr = net._tempo_rampa()
    ramp = np.minimum(1.0, np.asarray(net.eta, float)[:n]
                      / (np.asarray(_tr, float)[:n] if np.ndim(_tr) else _tr))
    grado = np.zeros(n, int)
    ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
    mm = (ii < n) & (jj < n)
    np.add.at(grado, ii[mm], 1); np.add.at(grado, jj[mm], 1)
    dent = dentro0[:n] if len(dentro0) >= n else np.pad(dentro0, (0, n - len(dentro0)))
    o = dict(passo=k, n=n, q=int(q),
             om_max=float(om.max()), om_p50=float(np.median(om)),
             om_top_p50=float(np.median(om[top])),
             # eta e ramp: sono APPENA NATI?
             eta_top_p50=float(np.median(net.eta[top])), eta_tutti_p50=float(np.median(net.eta[:n])),
             ramp_top_p50=float(np.median(ramp[top])), ramp_tutti_p50=float(np.median(ramp[:n])),
             ramp_top_min=float(ramp[top].min()),
             nati_dopo_zero_top=float(np.mean(top >= n0)),
             nati_dopo_zero_tutti=float(np.mean(np.arange(n) >= n0)),
             # inerzia: sono AL PAVIMENTO?
             rho_top_p50=float(np.median(rho[top])), rho_tutti_p50=float(np.median(rho[:n])),
             al_pav_top=float(np.mean(rho[top] <= PAV)),
             al_pav_tutti=float(np.mean(rho[:n] <= PAV)),
             inerzia_top_p50=float(np.median(inerzia[top])),
             # massa o vuoto?
             dentro_top=float(np.mean(dent[top])), dentro_tutti=float(np.mean(dent)),
             # topologia
             grado_top_p50=float(np.median(grado[top])), grado_tutti_p50=float(np.median(grado[:n])),
             isolati_top=float(np.mean(grado[top] == 0)))
    ris.append(o)

out = dict(FLAG=bool(FLAG), SEME=SEME, n0=n0, istanti=ris, traiettoria=trai, PAV=PAV)
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(out))
print("OK %s  max|omega| finale %.6g" % (NOME, trai[-1][1]))
'''


def braccio(nome, seme, flag):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nFLAG = %r\nPASSI = %d\n"
           "ISTANTI = %r\n" % (RADICE, TMP, nome, seme, SEP, flag, PASSI, list(ISTANTI))) + FIGLIO
    p = os.path.join(TMP, "_br_" + nome + ".py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


BR = [("mat_s%d" % s, s, True) for s in SEMI] + [("spe_s%d" % s, s, False) for s in SEMI]
proc = {n: braccio(n, s, f) for n, s, f in BR}
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


P("=" * 122)
P("**DOVE STA `omega` ESTREMO** — e la traiettoria del braccio SPENTO, che mancava")
P("=" * 122)
P()
P("  " + _passo.descrivi())
P("  scena (ii) (b), %d passi, %d semi, DUE bracci. Costo basso, per mandato." % (PASSI, len(SEMI)))
P()
P("  ❌ IL MIO CRITERIO ERA TROPPO LARGO, e Luca ha ragione: avevo chiesto «crescita in >= 95 %")
P("     dei passi» e con 0.023-0.143 ho concluso «non diverge». **Ma una successione puo'")
P("     crescere di x1000 salendo a scatti e scendendo spesso**: la monotonia e' SUFFICIENTE")
P("     per la divergenza, NON NECESSARIA. Il criterio giusto guarda IL LIVELLO, non la forma.")
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


D = {n: leggi(n) for n, _, _ in BR}
MAT = [D["mat_s%d" % s] for s in SEMI]
SPE = [D["spe_s%d" % s] for s in SEMI]

P("-" * 122)
P("A. LA TRAIETTORIA NEI DUE BRACCI — **il nullo è lo SPENTO**, e mancava")
P("-" * 122)
P("  %-7s %-26s %-26s %-22s" % ("passo", "max|omega|", "mediana |omega|", "max|phivel|"))
P("  %-7s %-12s %-13s %-12s %-13s %-10s %-11s" % ("", "MATURO", "SPENTO", "MATURO", "SPENTO",
                                                  "MATURO", "SPENTO"))
for k in (1, 5, 20, 60, 120):
    def _g(L, i):
        v = [next((t[i] for t in x["traiettoria"] if t[0] == k), None) for x in L]
        v = [y for y in v if y is not None]
        return float(np.median(v)) if v else float("nan")
    P("  %-7d %-12.6g %-13.6g %-12.6g %-13.6g %-10.6g %-11.6g"
      % (k, _g(MAT, 1), _g(SPE, 1), _g(MAT, 2), _g(SPE, 2), _g(MAT, 3), _g(SPE, 3)))
P()
for et, L in (("MATURO", MAT), ("SPENTO", SPE)):
    r = []
    for x in L:
        om = [t[1] for t in x["traiettoria"]]
        r.append(om[-1] / om[1] if len(om) > 1 and om[1] else float("nan"))
    P("  %-8s rapporto max|omega| (passo %d / passo 1), per seme: %s"
      % (et, PASSI, ", ".join("%.4g" % y for y in r)))
P()
_rm = np.median([[t[1] for t in x["traiettoria"]][-1] / [t[1] for t in x["traiettoria"]][1]
                 for x in MAT])
_rs = np.median([[t[1] for t in x["traiettoria"]][-1] / [t[1] for t in x["traiettoria"]][1]
                 for x in SPE])
P("  -> MATURO x%.4g   contro   SPENTO x%.4g      rapporto fra i due = %.4g"
  % (_rm, _rs, _rm / _rs if _rs else float("nan")))
if _rs > 10:
    P("     ** LA CRESCITA C'E' ANCHE A CAMPO SPENTO: NON VIENE DALLA `CURA 4`. **")
    P("     Il nullo dice che questo `omega` sale comunque, e la `CURA 4` non e' la causa.")
else:
    P("     ** LA CRESCITA E' DEL BRACCIO MATURO: il nullo (SPENTO) non la mostra. **")
P()
P("-" * 122)
P("B. DOVE STANNO — il top 0.1 %% per `|omega|`, contro TUTTI i nodi")
P("-" * 122)
for et, L in (("MATURO", MAT), ("SPENTO", SPE)):
    P("  braccio %s" % et)
    P("    %-6s %-6s %-12s %-24s %-24s %-22s %-20s"
      % ("passo", "top n", "|omega| top", "eta  (top / tutti)", "ramp (top / tutti)",
         "al pavimento (t/T)", "dentro massa (t/T)"))
    for k in ISTANTI:
        xs = [next((y for y in x["istanti"] if y["passo"] == k), None) for x in L]
        xs = [y for y in xs if y]
        if not xs:
            continue
        def m(c):
            return float(np.median([y[c] for y in xs]))
        P("    %-6d %-6.0f %-12.6g %-24s %-24s %-22s %-20s"
          % (k, m("q"), m("om_top_p50"),
             "%.4g / %.4g" % (m("eta_top_p50"), m("eta_tutti_p50")),
             "%.4f / %.4f" % (m("ramp_top_p50"), m("ramp_tutti_p50")),
             "%.4f / %.4f" % (m("al_pav_top"), m("al_pav_tutti")),
             "%.4f / %.4f" % (m("dentro_top"), m("dentro_tutti"))))
    P()
    P("    %-6s %-24s %-24s %-22s %-18s"
      % ("passo", "rho (top / tutti)", "grado (top / tutti)", "nati dopo 0 (t/T)", "isolati top"))
    for k in ISTANTI:
        xs = [next((y for y in x["istanti"] if y["passo"] == k), None) for x in L]
        xs = [y for y in xs if y]
        if not xs:
            continue
        def m(c):
            return float(np.median([y[c] for y in xs]))
        P("    %-6d %-24s %-24s %-22s %-18.4f"
          % (k, "%.4g / %.4g" % (m("rho_top_p50"), m("rho_tutti_p50")),
             "%.1f / %.1f" % (m("grado_top_p50"), m("grado_tutti_p50")),
             "%.4f / %.4f" % (m("nati_dopo_zero_top"), m("nati_dopo_zero_tutti")),
             m("isolati_top")))
    P()
P("-" * 122)
P("C. LA LETTURA — confrontando top e tutti, e i due bracci")
P("-" * 122)
kf = max(ISTANTI)
for et, L in (("MATURO", MAT), ("SPENTO", SPE)):
    xs = [next((y for y in x["istanti"] if y["passo"] == kf), None) for x in L]
    xs = [y for y in xs if y]
    if not xs:
        continue
    def m(c):
        return float(np.median([y[c] for y in xs]))
    P("  %s, al passo %d:" % (et, kf))
    for et2, a, b, dire in (
            ("APPENA NATI?", m("nati_dopo_zero_top"), m("nati_dopo_zero_tutti"),
             "i nodi nati DOPO il passo zero sono sovrarappresentati nel top"),
            ("INERZIA AL PAVIMENTO?", m("al_pav_top"), m("al_pav_tutti"),
             "il pavionmento `1e-6` morde piu' nel top"),
            ("DENTRO LE MASSE?", m("dentro_top"), m("dentro_tutti"),
             "il top sta nelle regioni coerenti")):
        _r = (a / b) if b else float("inf")
        P("     %-24s top %.4f  tutti %.4f   arricchimento x%.3g   %s"
          % (et2, a, b, _r, ("<- " + dire) if _r > 2.0 else ""))
    P("     `ramp` del top: %.4f contro %.4f di tutti   (`1` = maturo)"
      % (m("ramp_top_p50"), m("ramp_tutti_p50")))
    P("     `rho` del top: %.4g contro %.4g di tutti" % (m("rho_top_p50"), m("rho_tutti_p50")))
    P()
P("COSA QUESTO NON DICE:")
P("  - DUE SEMI e %d passi: non e' una barra d'errore, ed è di proposito (costo basso)." % PASSI)
P("  - NON dice se `omega` DIVERGA: dice DOVE sta il suo estremo. Il criterio sul LIVELLO")
P("    va riscritto, e questo è il materiale per scriverlo da una misura invece che da un modello.")
P("  - `nati dopo 0` usa l'INDICE del nodo come proxy dell'eta': vale perche' i nodi si")
P("    APPENDONO, ma **la mitosi RIMUOVE archi, non nodi**, quindi l'indice resta un proxy buono.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
