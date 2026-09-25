# -*- coding: utf-8 -*-
"""`SCALE-TW` **RIFATTO COL PASSO PIENO E IL CAMPO MATURO** *(mandato di Luca, 2026-09-25)*.

> *«`SCALE-TW` (b): `|tw|` su `4` semi, `300` passi, frazione nella finestra di creazione.
> «La mitosi è morta» resta SOSPESA fino ad allora.»*

**PERCHÉ IL PRIMO NON VALE:** avanzava con **`net.step()` da solo**, quindi **senza mitosi, senza
scuotimento del vuoto, senza memoria del moto** *(dove vivono il freno su `d0` e la gravità)*.
**La conclusione «la mitosi è morta» è quella che ha fatto riordinare il piano**, e va rifatta.

```
PRIMA (ciclo incompleto, 1 seme, 20 passi, campo spento):
   |tw| p50 fermo a 0.993 pi,  max 2.8991 pi,  frazione >= 3 pi = 0.000000
ORA: passo PIENO (`csv/_passo.py`), campo MATURO (`SEMINA_MATURA`), freno ON come il driver,
     4 SEMI, 300 PASSI.
```

**LA FINESTRA DI CREAZIONE SI DERIVA DAL CODICE**, non si scrive:
`soglia0 = PHI_CRIT + pi` se `TORS_4PI and not FASE_2PI`; creazione per
`soglia0 < avv < (centro-1)*PHI_CRIT` con `centro = (tau_soglia + tau_tetto)/2`.
**Misurata: `(1.500, 1.750) * PHI_CRIT`.**

**➕ E LA SORVEGLIANZA `A8-div` DI LUCA:** `max|omega_s|` e `max|phivel|` **per passo**.
**Se divergono → reperto e STOP**, e la diagnosi cerca **la causa che `TAU_A = 50` copriva**
*(candidato dichiarato: l'inerzia bloccata al pavimento)*, **e NON si rimette la rampa lenta.**
**«Diverge» si decide CONFRONTANDO i semi fra loro e la traiettoria con sé stessa**: crescita
quasi monotona senza plateau. **Il criterio è scritto QUI, prima dei numeri.**
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
FUORI = os.path.join(_QUI, "_scale_tw2")
DEST = os.path.join(FUORI, "SCALE_TW_passo_pieno.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEMI = [11, 12, 13, 14]
SEP = 4.0
PASSI = 300
ISTANTI = (0, 1, 5, 20, 60, 120, 200, 300)

FIGLIO = r'''
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import importlib.util as _iu
import _passo
_sp = _iu.spec_from_file_location("sim_tw2", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = True
S.SEMINA_MATURA = True          # CAMPO MATURO: la CURA 4
S.SCALA_MIN_PASSO = True        # come il driver
S.SCALA_MIN = False             # come il driver
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net

# LA FINESTRA, derivata dal codice
_s0 = (S.PHI_CRIT + np.pi) if (S.TORS_4PI and not S.FASE_2PI) else S.PHI_CRIT
TETTO = 4.0 * np.pi
_centro = 0.5 * ((1.0 + _s0 / S.PHI_CRIT) + (1.0 + TETTO / S.PHI_CRIT))
LO, HI = _s0, (_centro - 1.0) * S.PHI_CRIT

ris = []
trai = []
for k in range(PASSI + 1):
    if k:
        _passo.passo_pieno(S, net)
    _om = np.asarray(net.omega_s, float) if np.size(net.omega_s) else np.zeros((1, 3))
    trai.append((k,
                 float(np.max(np.linalg.norm(_om, axis=1))) if _om.size else float("nan"),
                 float(np.max(np.abs(net.phivel))) if np.size(net.phivel) else float("nan"),
                 int(net.n)))
    if k in ISTANTI:
        tw = np.abs(np.asarray(net.tw, float))
        ttw = S._tau_tw_locale(net) if S.TAU_LOCALI else S.TAU_TW
        ttw = np.asarray(ttw, float) * np.ones(len(net.d)) if np.ndim(ttw) == 0 \
            else np.asarray(ttw, float)
        o = dict(passo=k, n=int(net.n), archi=int(len(net.d)))
        if tw.size:
            o["tw_p50"] = float(np.median(tw)); o["tw_p95"] = float(np.percentile(tw, 95))
            o["tw_max"] = float(tw.max())
            o["fr_sopra_soglia"] = float(np.mean(tw >= LO))
            o["fr_nella_finestra"] = float(np.mean((tw >= LO) & (tw <= HI)))
            o["fr_sopra_tetto"] = float(np.mean(tw >= TETTO))
        o["ttw_p50"] = float(np.median(ttw))
        # LA MITOSI: quanti nodi sono nati?
        o["nati_mitosi"] = int(getattr(net, "_g_nati_mitosi", 0))
        o["eventi_mitosi"] = int(getattr(net, "_g_nati_mitosi_ev", 0))
        o["negate"] = int(getattr(net, "negate", -1))
        ris.append(o)

out = dict(seme=SEME, LO=float(LO), HI=float(HI), TETTO=float(TETTO), soglia0=float(_s0),
           PHI_CRIT=float(S.PHI_CRIT), istanti=ris, traiettoria=trai,
           g_rampa={k: (list(v) if isinstance(v, tuple) else v)
                    for k, v in vars(net).items()
                    if k.startswith("_g_rampa") and not k.endswith("_prec")},
           ordine=[n for _, n in _passo.ordine()])
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(out))
print("OK %s  n finale %d  nati_mitosi %d" % (NOME, net.n, getattr(net, "_g_nati_mitosi", 0)))
'''


def braccio(seme):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nPASSI = %d\nISTANTI = %r\n"
           % (RADICE, TMP, "s%d" % seme, seme, SEP, PASSI, list(ISTANTI))) + FIGLIO
    p = os.path.join(TMP, "_br_s%d.py" % seme)
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# I QUATTRO BRACCI IN PARALLELO: un processo per seme (`STANDARD 1`), e il tempo di muro
# resta quello di UNO.
proc = {s: braccio(s) for s in SEMI}
LOG = []
for s, pr in proc.items():
    so, se = pr.communicate()
    LOG.append("[s%d] rc=%d %s" % (s, pr.returncode,
                                   (so or b"").decode("utf-8", "replace").strip()[-140:]))
    if pr.returncode:
        LOG.append((se or b"").decode("utf-8", "replace")[-1500:])

P_ = []


def P(x=""):
    P_.append(x)


P("=" * 118)
P("`SCALE-TW` RIFATTO — PASSO PIENO, CAMPO MATURO, 4 SEMI, %d PASSI" % PASSI)
P("=" * 118)
P()
P("  " + _passo.descrivi())
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
U = D[SEMI[0]]
P("LA FINESTRA DI CREAZIONE, derivata dal codice:")
P("  soglia0 = %.6f = %.3f PHI_CRIT      tetto = %.6f = %.3f PHI_CRIT"
  % (U["soglia0"], U["soglia0"] / U["PHI_CRIT"], U["TETTO"], U["TETTO"] / U["PHI_CRIT"]))
P("  finestra: avv in (%.6f, %.6f) = (%.3f, %.3f) PHI_CRIT"
  % (U["LO"], U["HI"], U["LO"] / U["PHI_CRIT"], U["HI"] / U["PHI_CRIT"]))
P()
P("-" * 118)
P("%-6s %-7s %-8s %-10s %-10s %-10s %-12s %-12s %-10s"
  % ("passo", "n", "nati", "|tw|p50/pi", "p95/pi", "max/pi", ">=soglia", "in finestra", "_ttw p50"))
P("-" * 118)


def med(campo, k):
    v = [next((x[campo] for x in D[s]["istanti"] if x["passo"] == k and campo in x), None)
         for s in SEMI]
    v = [x for x in v if x is not None]
    return (float(np.mean(v)), float(np.std(v, ddof=1) / np.sqrt(len(v))) if len(v) > 1
            else float("nan")) if v else (float("nan"), float("nan"))


for k in ISTANTI:
    n_, _ = med("n", k)
    na_, _ = med("nati_mitosi", k)
    p50, _ = med("tw_p50", k)
    p95, _ = med("tw_p95", k)
    mx, _ = med("tw_max", k)
    fs, fse = med("fr_sopra_soglia", k)
    ff, ffe = med("fr_nella_finestra", k)
    tt, _ = med("ttw_p50", k)
    P("%-6d %-7.0f %-8.0f %-10.4f %-10.4f %-10.4f %-12.3e %-12.3e %-10.4f"
      % (k, n_, na_, p50 / np.pi, p95 / np.pi, mx / np.pi, fs, ff, tt))
P()
P("  (media su %d semi; `nati` = `_g_nati_mitosi` cumulativo)" % len(SEMI))
P()
P("=" * 118)
P("LA DOMANDA: **LA MITOSI E' MORTA?** — e ora il passo e' quello vero")
P("=" * 118)
kf = max(ISTANTI)
na_, nae = med("nati_mitosi", kf)
ev_, _ = med("eventi_mitosi", kf)
ff, ffe = med("fr_nella_finestra", kf)
fs, fse = med("fr_sopra_soglia", kf)
mx, mxe = med("tw_max", kf)
P("  al passo %d, media su %d semi:" % (kf, len(SEMI)))
P("     nodi nati da mitosi      = %.1f +- %.1f      eventi di mitosi = %.1f" % (na_, nae, ev_))
P("     frazione >= soglia0      = %.6e +- %.1e" % (fs, fse))
P("     frazione NELLA FINESTRA  = %.6e +- %.1e" % (ff, ffe))
P("     max |tw| / pi            = %.4f +- %.4f     (la soglia e' %.3f pi)"
  % (mx / np.pi, mxe / np.pi, U["soglia0"] / np.pi))
P()
if na_ > 0:
    P("  -> ** LA MITOSI NON E' MORTA: %.1f nodi nati in %d passi. **" % (na_, kf))
    P("     La conclusione precedente (\"max|tw| = 2.8991 pi, frazione 0.000000\") era misurata")
    P("     CON IL CICLO INCOMPLETO -- senza scuotimento e senza mitosi. VA RITIRATA.")
else:
    P("  -> la mitosi NON ha prodotto nodi in %d passi, col passo PIENO e il campo MATURO." % kf)
    P("     La conclusione precedente REGGE, e ora su un ciclo completo, 4 semi, %d passi." % kf)
P()
P("=" * 118)
P("`A8-div` — LA SORVEGLIANZA SULLA DIVERGENZA DI `omega` (criterio di Luca, scritto prima)")
P("=" * 118)
P("  Se `omega` diverge NON e' un risultato nuovo: `TAU_A = 50` ERA la cura \"per non far")
P("  divergere omega\" (help di `--tau-a`). Sarebbe IL DIFETTO ORIGINALE CHE TORNA FUORI.")
P()
P("  %-6s %-16s %-16s %-16s %-16s" % ("passo", "max|omega| p50", "max|omega| spread",
                                      "max|phivel| p50", "n p50"))
for k in (1, 20, 60, 120, 200, 300):
    vals = [next((t[1] for t in D[s]["traiettoria"] if t[0] == k), None) for s in SEMI]
    ph = [next((t[2] for t in D[s]["traiettoria"] if t[0] == k), None) for s in SEMI]
    nn = [next((t[3] for t in D[s]["traiettoria"] if t[0] == k), None) for s in SEMI]
    vals = [x for x in vals if x is not None]
    if not vals:
        continue
    P("  %-6d %-16.6g %-16.6g %-16.6g %-16.0f"
      % (k, float(np.median(vals)), float(np.max(vals) - np.min(vals)),
         float(np.median([x for x in ph if x is not None])),
         float(np.median([x for x in nn if x is not None]))))
P()
_cres = []
for s in SEMI:
    om = [t[1] for t in D[s]["traiettoria"]]
    _cres.append(sum(1 for a, b in zip(om, om[1:]) if b > a) / max(1, len(om) - 1))
P("  frazione di passi in CRESCITA di max|omega|, per seme: %s"
  % ", ".join("%.3f" % x for x in _cres))
_om_fin = [D[s]["traiettoria"][-1][1] for s in SEMI]
_om_ini = [D[s]["traiettoria"][1][1] for s in SEMI]
P("  rapporto finale/iniziale, per seme: %s"
  % ", ".join("%.4g" % (a / b if b else float("nan")) for a, b in zip(_om_fin, _om_ini)))
if all(x >= 0.95 for x in _cres):
    P("  -> ** DIVERGENZA: crescita quasi MONOTONA su TUTTI i semi. REPERTO E STOP. **")
    P("     La diagnosi cerca LA CAUSA CHE `TAU_A = 50` COPRIVA (candidato dichiarato:")
    P("     l'inerzia bloccata al pavimento `max(_rho_sorgente(), 1e-6)`, attiva sul 99.7 %")
    P("     dei nodi, par.9), E NON SI RIMETTE LA RAMPA LENTA.")
else:
    P("  -> NESSUNA DIVERGENZA con questo criterio: la crescita NON e' quasi monotona.")
    P("     E' un LIVELLO, non una divergenza.")
P()
P("CONTATORI DELLA RAMPA (`A8`), i CALI — per seme:")
for s in SEMI:
    P("  seme %-4d %s" % (s, D[s]["g_rampa"] or "NESSUNO"))
P()
P("COSA QUESTO NON DICE:")
P("  - la scena e' la (ii) (b), la piu' economica. La (a) non e' misurata qui.")
P("  - `4` semi soddisfano il minimo del par.0-ter, ma `t(3) = 3.18`: le barre sono larghe.")
P("  - la SOGLIA LOCALE e' modulata (fino a -30 %): la frazione vera e' >= a quella calcolata")
P("    contro `soglia0` fisso.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
