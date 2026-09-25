# -*- coding: utf-8 -*-
"""**IL LIMITE DI ACCOPPIAMENTO, RIFATTO IN CONFIGURAZIONE DEL DRIVER** *(ordine di Luca, 2026-09-25)*.

> **Perche' si rifa':** `CONFIG-1` ha misurato che la prima versione girava con **28 leggi su 31
> spente** — senza `FORK_SU2`, `CAMPO_SPINORIALE`, `CS_DINAMICO`, `TAU_LUCE`, `VERLET`… — cioe'
> **sul sistema pre-fork piu' due cure**. I numeri vecchi **restano** e si stampano accanto ai
> nuovi, marcati: **non si cancella una misura, si dichiara di quale sistema era.**

**COSA CAMBIA rispetto alla prima versione, punto per punto** *(tutti requisiti di Luca)*:

| | prima | **ora** |
|---|---|---|
| configurazione | 4 flag a mano | **argv del DRIVER**, catturata (`_cli_flag`) |
| bersagli | **1** nodo per seme | **>= 20** nodi per seme |
| verso del taglio | solo i piu' **LUNGHI** via | **ENTRAMBI** i versi |
| `RAMPA-1` | assente (`eta = _tempo_rampa()`) | **attiva** (`eta = +inf`) |
| configurazione nel referto | i 4 flag toccati | **tutti i 78 booleani** (`P5`) |

**PERCHE' I DUE VERSI:** togliere i piu' **lunghi** e' il taglio meno invasivo sul kernel
`exp(-d/lam)`; togliere i piu' **corti** toglie il vicinato che pesa di piu'. **Se il crollo
dell'inerzia c'e' in ENTRAMBI i versi, non e' un artefatto della scelta del taglio** — ed e'
esattamente il dubbio che un solo verso lasciava aperto.

**COME SI OTTENGONO 20 BERSAGLI SENZA 20 COPIE PER `k`:** i bersagli si scelgono **NON ADIACENTI
fra loro**, quindi **nessun arco viene tolto due volte** e un solo taglio serve per tutti.
**⚠ LIMITE DICHIARATO:** due bersagli non adiacenti possono **condividere un VICINO**, quindi
l'effetto del taglio **non e' perfettamente indipendente** fra bersagli. E' il prezzo di avere
20 nodi invece di 1, e va detto invece di far sembrare i 20 campioni indipendenti.

**COPPIA e INERZIA sono variabili LOCALI di `_passo_spinoriale`**, quindi non si leggono da
fuori: si usa una **COPIA del simulatore con quattro assegnazioni diagnostiche**, il file vero
**non si tocca**, e **i blob di entrambi vanno nel referto** (par.5-quinquies).

**IL CRITERIO, SCRITTO PRIMA:** *se `|coppia|` resta dello stesso ordine e `inerzia` CROLLA al
calare di `k`, `omega` esplode **per la legge dell'inerzia**, non per il nodo.* `|omega|` e' il
**controllo**: se esplode anche lui, la catena e' quella; se non si muove, il rapporto misurato
non arriva alla dinamica.

**Sola lettura sul simulatore. Nessuna cura.**
"""
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
FUORI = os.path.join(_QUI, "_limite_accoppiamento2")
DEST = os.path.join(FUORI, "LIMITE_ACCOPPIAMENTO2.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)
NL = chr(10)

SEMI = [11, 12]
SEP = 4.0
GRADI = [77, 20, 8, 4, 2]
VERSI = ["lunghi", "corti"]
PASSI_PRIMA = 20
BERSAGLI = 20

# I NUMERI VECCHI, dal referto della prima versione: NON si ricopiano a mano dalla memoria,
# si leggono dal FILE (`P1-ter`). Se il file non c'e', si dice, invece di inventarli.
VECCHIO_FILE = os.path.join(_QUI, "_limite_accoppiamento", "LIMITE_ACCOPPIAMENTO.txt")


def numeri_vecchi():
    try:
        t = io.open(VECCHIO_FILE, encoding="utf-8", errors="replace").read()
    except Exception as e:
        return None, "il referto vecchio non e' leggibile (%s)" % e
    fuori = {}
    for r in t.split(NL):
        p = r.split()
        if len(p) >= 6 and p[0].isdigit() and p[1].isdigit():
            try:
                fuori[int(p[0])] = dict(grado=int(p[1]), coppia=float(p[2]),
                                        inerzia=float(p[3]), rapporto=float(p[4]),
                                        omega=float(p[5]))
            except ValueError:
                pass
    return (fuori or None), ("letti %d valori di `k`" % len(fuori) if fuori
                            else "nessuna riga numerica riconosciuta")


# ------------------------------------------------- LA COPIA con le assegnazioni diagnostiche
SIM = os.path.join(RADICE, "soliton_simulator.py")
COPIA = os.path.join(FUORI, "_sim_diag2.py")
src = io.open(SIM, encoding="utf-8", newline="").read()
blob_vero = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()[:8]

A = "        inerzia = np.maximum(_contrasto * _T2, 1e-6)       # il pavimento RESTA"
assert src.count(A) == 1, "l'ancora dell'inerzia non e' unica: %d" % src.count(A)
src2 = src.replace(A, NL.join([
    "        inerzia = np.maximum(_contrasto * _T2, 1e-6)",
    "        self._diag_inerzia = np.array(inerzia, copy=True)  # DIAGNOSTICO",
    "        self._diag_contrasto = np.array(_contrasto, copy=True)",
    "        self._diag_T2 = np.array(_T2, copy=True)",
    "        _ = 1  # il pavimento RESTA"]), 1)
B = "        omega_new = omega_src + dtn_c * (correzione / inerzia[:, None] - omega_src / _tau)"
assert src2.count(B) == 1, "l'ancora di omega_new non e' unica"
src2 = src2.replace(B, "        self._diag_coppia = np.array(correzione, copy=True)  # DIAGNOSTICO"
                    + NL + B, 1)
io.open(COPIA, "w", encoding="utf-8", newline=NL).write(src2)
blob_copia = hashlib.sha1(io.open(COPIA, "rb").read()).hexdigest()[:8]

# ------------------------------------------------- l'argv VERA del driver
_S0, ARGV = _cli_flag.argv_del_driver([], dest=os.path.join(TMP, "_scarto"))
ARGV = ARGV + ["--nodi", "0"]     # il vuoto di `_applica_flag` non si usa: la scena e' la (ii)

FIGLIO = r'''
import copy as _copy
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import _cli_flag
import _passo
_argv, _scartate = _cli_flag.argv_per(COPIA, ARGV)
S, _a = _cli_flag.carica_dal_cli(_argv, nome="sim_la2", sim=COPIA)
_CFG = {"scartate": _scartate, "argv_len": len(_argv),
        "SEMINA_MATURA": bool(getattr(S, "SEMINA_MATURA", False)),
        "CS_DINAMICO": bool(getattr(S, "CS_DINAMICO", False)),
        "FORK_SU2": bool(getattr(S, "FORK_SU2", False)),
        "TAU_LUCE": bool(getattr(S, "TAU_LUCE", False))}
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
for _ in range(PASSI_PRIMA):
    _passo.passo_pieno(S, net)

n = int(net.n)
ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
mm = (ii < n) & (jj < n)
grado = np.zeros(n, int)
np.add.at(grado, ii[mm], 1); np.add.at(grado, jj[mm], 1)
gm = int(np.median(grado))
# I BERSAGLI: grado >= max(GRADI) (senno' `k = 77` non e' raggiungibile) e NON ADIACENTI fra
#   loro, cosi' nessun arco e' tolto due volte e un solo taglio serve per tutti.
_ok = np.where(grado >= max(GRADI))[0]
_ok = _ok[np.argsort(np.abs(grado[_ok] - gm))]       # i piu' TIPICI per primi
vic = {}
for _k in range(len(net.d)):
    if not mm[_k]:
        continue
    vic.setdefault(int(ii[_k]), set()).add(int(jj[_k]))
    vic.setdefault(int(jj[_k]), set()).add(int(ii[_k]))
BERS, presi = [], set()
for _c in _ok:
    _c = int(_c)
    if _c in presi:
        continue
    BERS.append(_c)
    presi.add(_c); presi |= vic.get(_c, set())
    if len(BERS) >= BERSAGLI:
        break

d = np.asarray(net.d, float)
suoi = {b: np.where((ii == b) | (jj == b))[0] for b in BERS}
o = dict(SEME=SEME, VERSO=VERSO, n=n, grado_mediano=gm, CFG=_CFG,
         bersagli=[int(b) for b in BERS], gradi=[int(grado[b]) for b in BERS], casi=[])

for K in GRADI:
    net2 = _copy.deepcopy(net)
    via = set()
    for b in BERS:
        s = suoi[b]
        ordine = s[np.argsort(d[s])]                 # dal piu' CORTO al piu' lungo
        if VERSO == "lunghi":
            ordine = ordine[::-1]                    # via i piu' LUNGHI per primi
        via |= set(int(x) for x in ordine[:max(0, s.size - K)])
    keep = np.array([k not in via for k in range(len(net2.d))], bool)
    for _nome in list(vars(net2)):
        _v = getattr(net2, _nome)
        if isinstance(_v, np.ndarray) and _v.ndim >= 1 and _v.shape[0] == keep.size:
            setattr(net2, _nome, _v[keep])
    net2._S = None; net2._perm = None; net2._ker_cache = None; net2._cicli_topologici = None
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
        B = np.array([b for b in BERS if b < _in.size and b < _om.size], int)
        cop = np.linalg.norm(_co[B], axis=1) if _co.size else np.zeros(0)
        c = dict(K=int(K), quanti=int(B.size), archi_rimasti=int(keep.sum()),
                 grado_p50=float(np.median(_g[B])) if B.size else float("nan"),
                 coppia_p50=float(np.median(cop)) if cop.size else float("nan"),
                 inerzia_p50=float(np.median(_in[B])) if B.size else float("nan"),
                 contrasto_p50=float(np.median(_ct[B])) if B.size and _ct.size else float("nan"),
                 T2_p50=float(np.median(_t2[B])) if B.size and _t2.size else float("nan"),
                 omega_p50=float(np.median(_om[B])) if B.size else float("nan"),
                 al_pavimento=int(np.sum(_in[B] <= 1e-6)) if B.size else -1)
        if cop.size and B.size:
            _r = cop / np.maximum(_in[B], 1e-300)
            c["rapporto_p50"] = float(np.median(_r))
            c["rapporto_min"] = float(_r.min()); c["rapporto_max"] = float(_r.max())
        o["casi"].append(c)
    except Exception as e:
        o["casi"].append(dict(K=int(K), errore=str(e)[:200]))

io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  bersagli %d  casi %d" % (NOME, len(BERS), len(o["casi"])))
'''


def braccio(seme, verso):
    nome = "s%d_%s" % (seme, verso)
    testa = ["RAD = %r" % RADICE, "TMPD = %r" % TMP, "NOME = %r" % nome,
             "SEME = %d" % seme, "SEP = %r" % SEP, "COPIA = %r" % COPIA,
             "GRADI = %r" % GRADI, "PASSI_PRIMA = %d" % PASSI_PRIMA,
             "BERSAGLI = %d" % BERSAGLI, "VERSO = %r" % verso, "ARGV = %r" % ARGV, ""]
    p = os.path.join(TMP, "_br_%s.py" % nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(NL.join(testa) + FIGLIO)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


LOG = []
proc = {}
for s in SEMI:
    for v in VERSI:
        proc[(s, v)] = braccio(s, v)        # UN PROCESSO PER BRACCIO (`STANDARD 1`)
for (s, v), pr in proc.items():
    so, se = pr.communicate()
    LOG.append("[s%d %s] rc=%d %s" % (s, v, pr.returncode,
                                      (so or b"").decode("utf-8", "replace").strip()[-120:]))
    if pr.returncode:
        LOG.append((se or b"").decode("utf-8", "replace")[-1500:])

R = []


def P(s=""):
    R.append(s)


P("=" * 120)
P("IL LIMITE DI ACCOPPIAMENTO -- RIFATTO IN CONFIGURAZIONE DEL DRIVER   (2026-09-25)")
P("=" * 120)
P()
for l in LOG:
    P(l)
P()
P("blob del simulatore VERO   %s" % blob_vero)
P("blob della COPIA diagnostica  %s   (4 assegnazioni, il file vero NON e' toccato)" % blob_copia)
P("semi %s   versi del taglio %s   k %s   bersagli per seme %d   passi pieni prima %d"
  % (SEMI, VERSI, GRADI, BERSAGLI, PASSI_PRIMA))
P()

# --------------------------------------------------------------- `P5`: la configurazione INTERA
_Sq, _ = _cli_flag.carica_dal_cli(_cli_flag.argv_per(COPIA, ARGV)[0], nome="cfg_la2", sim=COPIA)
_in_conf = _cli_flag.dichiara_configurazione(_Sq, P)


def leggi(nome):
    try:
        return json.loads(io.open(os.path.join(TMP, nome + ".json"), encoding="utf-8").read())
    except Exception:
        return None


VEC, nota_vec = numeri_vecchi()
P("=" * 120)
P("I NUMERI, e accanto quelli VECCHI -- marcati **sistema pre-fork + 2 cure** (`CONFIG-1`)")
P("=" * 120)
P("  (i numeri vecchi sono LETTI dal referto della prima versione, non ricopiati: %s)" % nota_vec)
P()
tabelle = {}
for s in SEMI:
    for v in VERSI:
        o = leggi("s%d_%s" % (s, v))
        if not o:
            P("  [s%d %s] NESSUN DATO" % (s, v))
            continue
        tabelle[(s, v)] = o
        P("-" * 120)
        P("SEME %d   taglio: via i piu' %s   n = %d   grado mediano %d   bersagli %d"
          % (s, v.upper(), o["n"], o["grado_mediano"], len(o["bersagli"])))
        P("  configurazione del figlio: SEMINA_MATURA %s  CS_DINAMICO %s  FORK_SU2 %s  TAU_LUCE %s"
          % (o["CFG"]["SEMINA_MATURA"], o["CFG"]["CS_DINAMICO"], o["CFG"]["FORK_SU2"],
             o["CFG"]["TAU_LUCE"]))
        P("-" * 120)
        P("%-6s %-8s %-14s %-14s %-16s %-14s %-14s %-9s | %s"
          % ("k", "grado", "COPPIA p50", "INERZIA p50", "coppia/inerzia", "|omega| p50",
             "contrasto", "al pav.", "VECCHIO coppia/inerzia"))
        for c in o["casi"]:
            if "errore" in c:
                P("%-6s ERRORE: %s" % (c["K"], c["errore"]))
                continue
            vv = (VEC or {}).get(c["K"])
            P("%-6d %-8.1f %-14.6g %-14.6g %-16.6g %-14.6g %-14.6g %-9s | %s"
              % (c["K"], c["grado_p50"], c["coppia_p50"], c["inerzia_p50"],
                 c.get("rapporto_p50", float("nan")), c["omega_p50"], c["contrasto_p50"],
                 "%d/%d" % (c["al_pavimento"], c["quanti"]),
                 ("%.6g" % vv["rapporto"]) if vv else "--"))
        P()

P("=" * 120)
P("COME SCALANO IN `k` -- pendenza su `log k` (COPPIA e INERZIA SEPARATE, come chiesto)")
P("=" * 120)
P("%-14s %-16s %-16s %-16s %-16s" % ("braccio", "pend. COPPIA", "pend. INERZIA",
                                     "pend. rapporto", "pend. |omega|"))


def pend(xs, ys):
    xs = np.log(np.asarray(xs, float)); ys = np.asarray(ys, float)
    m = np.isfinite(ys) & (ys > 0)
    if m.sum() < 3:
        return float("nan")
    return float(np.polyfit(xs[m], np.log(ys[m]), 1)[0])


pendenze = {}
for (s, v), o in sorted(tabelle.items()):
    ks = [c["K"] for c in o["casi"] if "errore" not in c]
    gc = lambda nome: [c[nome] for c in o["casi"] if "errore" not in c]
    pc, pi = pend(ks, gc("coppia_p50")), pend(ks, gc("inerzia_p50"))
    pr = pend(ks, [c.get("rapporto_p50", float("nan")) for c in o["casi"] if "errore" not in c])
    po = pend(ks, gc("omega_p50"))
    pendenze[(s, v)] = (pc, pi, pr, po)
    P("%-14s %-16.4f %-16.4f %-16.4f %-16.4f" % ("s%d %s" % (s, v), pc, pi, pr, po))
P()
P("  Una pendenza POSITIVA su `log k` significa: la grandezza CRESCE col grado. Per l'inerzia")
P("  una pendenza ~ +1 direbbe `inerzia ~ k`; per la coppia ~ 0 direbbe INTENSIVA.")
P("  *(La coerenza che Luca chiede: se la coppia e' intensiva, l'inerzia DEVE esserlo.)*")
P()

P("=" * 120)
P("IL CRITERIO, scritto PRIMA: se `|coppia|` resta dello stesso ordine e `inerzia` CROLLA al")
P("calare di `k`, `omega` esplode PER LA LEGGE DELL'INERZIA, non per il nodo. `|omega|` e' il")
P("CONTROLLO.")
P("=" * 120)
esiti = []
for (s, v), o in sorted(tabelle.items()):
    cc = [c for c in o["casi"] if "errore" not in c]
    if len(cc) < 2:
        continue
    a, b = cc[0], cc[-1]
    rc = b["coppia_p50"] / a["coppia_p50"] if a["coppia_p50"] else float("nan")
    ri = b["inerzia_p50"] / a["inerzia_p50"] if a["inerzia_p50"] else float("nan")
    rr = (b.get("rapporto_p50", float("nan")) / a["rapporto_p50"]) if a.get("rapporto_p50") \
        else float("nan")
    ro = b["omega_p50"] / a["omega_p50"] if a["omega_p50"] else float("nan")
    esiti.append((s, v, rc, ri, rr, ro))
    P("  s%d %-8s da k = %d a k = %d:  COPPIA x%-10.4g INERZIA x%-10.4g rapporto x%-10.4g |omega| x%.4g"
      % (s, v, a["K"], b["K"], rc, ri, rr, ro))
P()
_crolla = [e for e in esiti if np.isfinite(e[3]) and e[3] < 0.5]
_coppia_ferma = [e for e in esiti if np.isfinite(e[2]) and e[2] < 5.0]
if len(_crolla) == len(esiti) and len(esiti) and len(_coppia_ferma) == len(esiti):
    P("  -> LA LEGGE DELL'INERZIA NON REGGE IL LIMITE, **IN TUTTI E %d I BRACCI**" % len(esiti))
    P("     (due semi x due versi del taglio): la coppia resta dello stesso ordine e l'inerzia")
    P("     CROLLA. **Il verso del taglio NON e' il responsabile**, ed era il dubbio che la")
    P("     prima versione, con un solo verso, lasciava aperto.")
else:
    P("  -> IL QUADRO NON E' UNIFORME FRA I BRACCI: %d su %d con inerzia in crollo, %d su %d"
      % (len(_crolla), len(esiti), len(_coppia_ferma), len(esiti)))
    P("     con coppia ferma. **Va letto braccio per braccio**, e il verso del taglio potrebbe")
    P("     contare: e' un risultato diverso da quello della prima versione, e va detto.")
P()
P("=" * 120)
P("COSA QUESTO NON DICE")
P("=" * 120)
P("  - i 20 bersagli NON sono adiacenti fra loro (nessun arco tolto due volte), **ma possono")
P("    condividere un VICINO**: l'effetto del taglio non e' perfettamente indipendente fra")
P("    bersagli. E' il prezzo di averne 20 invece di 1, e si dichiara.")
P("  - il taglio TOGLIE ARCHI A MANO: non e' un processo del sistema, ed e' di proposito -- la")
P("    domanda e' se la LEGGE regga un `k` piccolo, non se il sistema ci arrivi da solo.")
P("  - DUE SEMI: la dispersione fra semi si legge dalle due righe, non da una barra (`P3` delle")
P("    regole: per una barra servono >= 4 semi).")
P("  - SOLA LETTURA sul simulatore: la copia diagnostica NON e' il file delle campagne, e i due")
P("    blob sono in testa.")
P("  - i numeri VECCHI sono di un ALTRO SISTEMA (`CONFIG-1`: 28 leggi su 31 spente). Il")
P("    confronto e' fra due sistemi, **non** una ripetizione della stessa misura.")

T = NL.join(R) + NL
os.makedirs(FUORI, exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
sys.exit(0)
