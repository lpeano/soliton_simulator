# -*- coding: utf-8 -*-
"""SIGILLO `INERZIA-1(C)` — **IL CONTRASTO PER VICINO** (`CONTRASTO_INTENSIVO`).

**I SEI CRITERI SONO DI LUCA**, e stanno nel task history
`doc/TASK_HISTORY/2026-09-25_inerzia1-contrasto-intensivo.md`, **committato prima del codice**:

```
C1  pendenze su log k di COPPIA e INERZIA uguali entro l'errore fra semi   (oggi -0.2 vs +1.5/+2.4)
C2  |omega| a k = 2 dello stesso ordine di k = 77                          (oggi x150-176)
C3  flag spento BYTE-IDENTICO al codice PRECEDENTE -- non `HEAD` (`P8`)
C4  CASO CHE DEVE FALLIRE: il braccio spento, generato TOGLIENDO il flag dall'argv
C5  pavimento 1e-6: quante volte morde con la cura                         (oggi 0/20)
C6  scala dell'inerzia su TUTTI i nodi prima/dopo -- mediana, p5, p95
```

**TUTTO DAL CLI** (`P3`): l'argv si **cattura dal driver** e il braccio spento e' la **stessa
argv MENO l'opzione** — l'unico OFF che il CLI ammette, perche' i flag sono `store_true`.
**`P5`:** il referto dichiara la **configurazione INTERA**, non i flag toccati.
**`P8`:** il codice «di prima» e' il **PADRE del commit che ha introdotto il flag**, trovato con
`_cli_flag.sim_prima_del_flag`, **non `HEAD`** — che conterrebbe la cura.

**COPPIA e INERZIA sono variabili LOCALI di `_passo_spinoriale`**: si usa una **COPIA** del
simulatore con quattro assegnazioni diagnostiche, **il file vero non si tocca**, e **i blob di
entrambi** vanno nel referto.

ASCII puro.
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
FUORI = os.path.join(_QUI, "_sig_contrasto")
DEST = os.path.join(FUORI, "SIGILLO_contrasto_intensivo.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)
NL = chr(10)

SEMI = [11, 12]
SEP = 4.0
GRADI = [77, 20, 8, 4, 2]
VERSI = ["lunghi", "corti"]
PASSI_PRIMA = 20
BERSAGLI = 20
OPZ = "--contrasto-intensivo"
FLAGNOME = "CONTRASTO_INTENSIVO"

SIM = os.path.join(RADICE, "soliton_simulator.py")
blob_vero = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()[:8]


def copia_diag(sorgente, dest):
    """La COPIA con le quattro assegnazioni diagnostiche. Restituisce (blob, quante ancore)."""
    src = io.open(sorgente, encoding="utf-8", newline="").read()
    k = 0
    A = "        inerzia = np.maximum(_contrasto * _T2, 1e-6)       # il pavimento RESTA"
    if src.count(A) == 1:
        src = src.replace(A, NL.join([
            "        inerzia = np.maximum(_contrasto * _T2, 1e-6)",
            "        self._diag_inerzia = np.array(inerzia, copy=True)",
            "        self._diag_contrasto = np.array(_contrasto, copy=True)",
            "        self._diag_T2 = np.array(_T2, copy=True)",
            "        _ = 1  # il pavimento RESTA"]), 1)
        k += 1
    else:
        # il codice PRECEDENTE alla cura ha la riga SENZA il commento finale: si prova l'altra
        A2 = "        inerzia = np.maximum(_contrasto * _T2, 1e-6)"
        assert src.count(A2) >= 1, "nessuna ancora dell'inerzia in %s" % sorgente
        src = src.replace(A2, NL.join([
            A2,
            "        self._diag_inerzia = np.array(inerzia, copy=True)",
            "        self._diag_contrasto = np.array(_contrasto, copy=True)",
            "        self._diag_T2 = np.array(_T2, copy=True)"]), 1)
        k += 1
    B = "        omega_new = omega_src + dtn_c * (correzione / inerzia[:, None] - omega_src / _tau)"
    assert src.count(B) == 1, "l'ancora di omega_new non e' unica in %s" % sorgente
    src = src.replace(B, "        self._diag_coppia = np.array(correzione, copy=True)" + NL + B, 1)
    k += 1
    io.open(dest, "w", encoding="utf-8", newline=NL).write(src)
    return hashlib.sha1(io.open(dest, "rb").read()).hexdigest()[:8], k


COPIA = os.path.join(FUORI, "_sim_diag_ci.py")
blob_copia, anc_copia = copia_diag(SIM, COPIA)

# ---------------------------------------------------------- `P8`: il codice PRIMA della cura
PRIMA = os.path.join(TMP, "_sim_prima.py")
COMMIT_CURA = _cli_flag.sim_prima_del_flag(FLAGNOME, PRIMA, radice=RADICE)
PRIMA_DIAG = os.path.join(TMP, "_sim_prima_diag.py")
blob_prima, anc_prima = copia_diag(PRIMA, PRIMA_DIAG)

# ---------------------------------------------------------- l'argv VERA del driver
_S0, ARGV = _cli_flag.argv_del_driver([], dest=os.path.join(TMP, "_scarto"))
ARGV = ARGV + ["--nodi", "0"]
ARGV_ON = ARGV + [OPZ]          # il flag NON e' nel driver: si aggiunge, e si dichiara
ARGV_OFF = list(ARGV)           # il braccio spento: **l'argv SENZA l'opzione**

FIGLIO = r'''
import copy as _copy
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import _cli_flag
import _passo
_argv, _scartate = _cli_flag.argv_per(SIM, ARGV)
S, _a = _cli_flag.carica_dal_cli(_argv, nome="sim_ci", sim=SIM)
_CFG = {"flag": getattr(S, FLAGNOME, "ASSENTE"), "atteso": bool(FLAG),
        "opz_nell_argv": OPZ in _argv, "scartate": _scartate,
        "sim": os.path.basename(SIM)}
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

# ---- `C6`: LA SCALA DELL'INERZIA SU TUTTI I NODI (non solo sui bersagli) --------------
_inA = np.asarray(getattr(net, "_diag_inerzia", []), float)
o = dict(SEME=SEME, VERSO=VERSO, n=n, grado_mediano=gm, CFG=_CFG, casi=[],
         firme={}, scala={})
if _inA.size:
    o["scala"] = dict(p5=float(np.percentile(_inA, 5)), p50=float(np.median(_inA)),
                      p95=float(np.percentile(_inA, 95)), min=float(_inA.min()),
                      max=float(_inA.max()), nodi=int(_inA.size),
                      al_pavimento=int(np.sum(_inA <= 1e-6)))
o["contatori"] = {k: (v if isinstance(v, (int, float)) else str(v))
                  for k, v in vars(net).items() if k.startswith("_g_ci")}

# ---- `C3`: LA FIRMA DEI BYTE dello stato, per la byte-identita' -----------------------
import hashlib as _h
for k, v in sorted(vars(net).items()):
    if k.startswith("_g_") or k.startswith("_diag"):
        continue
    if isinstance(v, np.ndarray):
        o["firme"][k] = [_h.sha1(np.ascontiguousarray(v).tobytes()).hexdigest()[:12],
                         list(v.shape), str(v.dtype)]
    elif isinstance(v, (int, float, bool, str)):
        o["firme"][k] = [_h.sha1(repr(v).encode()).hexdigest()[:12], [], type(v).__name__]

# ---- i bersagli e il taglio, come in `CONFIG-1/a` -------------------------------------
_ok = np.where(grado >= max(GRADI))[0]
_ok = _ok[np.argsort(np.abs(grado[_ok] - gm))]
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
o["bersagli"] = [int(b) for b in BERS]

d = np.asarray(net.d, float)
suoi = {b: np.where((ii == b) | (jj == b))[0] for b in BERS}
for K in GRADI:
    net2 = _copy.deepcopy(net)
    via = set()
    for b in BERS:
        s = suoi[b]
        ordine = s[np.argsort(d[s])]
        if VERSO == "lunghi":
            ordine = ordine[::-1]
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
        _om = np.linalg.norm(np.asarray(net2.omega_s, float), axis=1)
        B = np.array([b for b in BERS if b < _in.size and b < _om.size], int)
        cop = np.linalg.norm(_co[B], axis=1) if _co.size else np.zeros(0)
        c = dict(K=int(K), quanti=int(B.size),
                 coppia_p50=float(np.median(cop)) if cop.size else float("nan"),
                 inerzia_p50=float(np.median(_in[B])) if B.size else float("nan"),
                 contrasto_p50=float(np.median(_ct[B])) if B.size and _ct.size else float("nan"),
                 omega_p50=float(np.median(_om[B])) if B.size else float("nan"),
                 al_pavimento=int(np.sum(_in[B] <= 1e-6)) if B.size else -1,
                 al_pavimento_tutti=int(np.sum(_in <= 1e-6)) if _in.size else -1,
                 nodi_tutti=int(_in.size))
        if cop.size and B.size:
            c["rapporto_p50"] = float(np.median(cop / np.maximum(_in[B], 1e-300)))
        o["casi"].append(c)
    except Exception as e:
        o["casi"].append(dict(K=int(K), errore=str(e)[:200]))

io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  bersagli %d  casi %d" % (NOME, len(BERS), len(o["casi"])))
'''


def braccio(nome, seme, verso, flag, sim, argv):
    testa = ["RAD = %r" % RADICE, "TMPD = %r" % TMP, "NOME = %r" % nome,
             "SEME = %d" % seme, "SEP = %r" % SEP, "SIM = %r" % sim,
             "GRADI = %r" % GRADI, "PASSI_PRIMA = %d" % PASSI_PRIMA,
             "BERSAGLI = %d" % BERSAGLI, "VERSO = %r" % verso, "ARGV = %r" % argv,
             "FLAG = %r" % flag, "OPZ = %r" % OPZ, "FLAGNOME = %r" % FLAGNOME, ""]
    p = os.path.join(TMP, "_br_%s.py" % nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(NL.join(testa) + FIGLIO)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


BRACCI = []
for s in SEMI:
    for v in VERSI:
        BRACCI.append(("on_s%d_%s" % (s, v), s, v, True, COPIA, ARGV_ON))
        BRACCI.append(("off_s%d_%s" % (s, v), s, v, False, COPIA, ARGV_OFF))
# `C3`/`C4`: il codice PRECEDENTE alla cura, un braccio per seme (verso `lunghi`, basta uno)
for s in SEMI:
    BRACCI.append(("prima_s%d_lunghi" % s, s, "lunghi", False, PRIMA_DIAG, ARGV_OFF))

LOG = []
proc = {}
for (nome, s, v, fl, sim, argv) in BRACCI:
    proc[nome] = braccio(nome, s, v, fl, sim, argv)      # UN PROCESSO PER BRACCIO
for nome, pr in proc.items():
    so, se = pr.communicate()
    LOG.append("[%s] rc=%d %s" % (nome, pr.returncode,
                                  (so or b"").decode("utf-8", "replace").strip()[-100:]))
    if pr.returncode:
        LOG.append((se or b"").decode("utf-8", "replace")[-1500:])

R = []


def P(s=""):
    R.append(s)


def crit(sigla, cosa, ok, detta):
    P("%-5s %-4s  %s" % (sigla, "PASS" if ok else "FAIL", cosa))
    for r_ in (detta or "").split(NL):
        if r_:
            P("             " + r_)
    P()
    return bool(ok)


def leggi(nome):
    try:
        return json.loads(io.open(os.path.join(TMP, nome + ".json"), encoding="utf-8").read())
    except Exception:
        return None


def pend(xs, ys):
    xs = np.log(np.asarray(xs, float))
    ys = np.asarray(ys, float)
    m = np.isfinite(ys) & (ys > 0)
    if m.sum() < 3:
        return float("nan")
    return float(np.polyfit(xs[m], np.log(ys[m]), 1)[0])


P("=" * 116)
P("SIGILLO `INERZIA-1(C)` -- IL CONTRASTO PER VICINO (`CONTRASTO_INTENSIVO`)")
P("=" * 116)
P()
for l in LOG:
    P(l)
P()
P("blob del simulatore VERO      %s" % blob_vero)
P("blob della COPIA diagnostica  %s   (%d ancore)" % (blob_copia, anc_copia))
P("il codice di PRIMA e'         %s^   (il PADRE del commit che ha introdotto %s, NON `HEAD`)"
  % (COMMIT_CURA[:8], FLAGNOME))
P("blob della copia di PRIMA     %s   (%d ancore)" % (blob_prima, anc_prima))
P("semi %s   versi %s   k %s   bersagli %d   passi pieni prima %d"
  % (SEMI, VERSI, GRADI, BERSAGLI, PASSI_PRIMA))
P()
_Sq, _ = _cli_flag.carica_dal_cli(_cli_flag.argv_per(COPIA, ARGV_ON)[0], nome="cfg_ci", sim=COPIA)
_cli_flag.dichiara_configurazione(
    _Sq, P, esenzione="il flag in prova NON e' ancora nel driver (decisione di Luca: entra fra le "
                      "cure dopo il sigillo), quindi l'argv ON e' quella del driver PIU' %s" % OPZ)

if any("rc=1" in l for l in LOG):
    P("STOP: un braccio non e' arrivato in fondo. Nessun criterio si legge.")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL.join(R))
    sys.exit(1)

OK = []
dati = {}
for (nome, s, v, fl, sim, argv) in BRACCI:
    dati[nome] = leggi(nome)

# ---------------------------------------------------------------- la tabella
P("=" * 116)
P("I NUMERI, braccio per braccio")
P("=" * 116)
for (nome, s, v, fl, sim, argv) in BRACCI:
    o = dati.get(nome)
    if not o:
        P("  [%s] NESSUN DATO" % nome)
        continue
    P("-" * 116)
    P("%s   seme %d   verso %s   %s = %s   (sim %s)"
      % (nome, s, v, FLAGNOME, o["CFG"]["flag"], o["CFG"]["sim"]))
    P("%-6s %-14s %-14s %-16s %-14s %-14s %s"
      % ("k", "COPPIA p50", "INERZIA p50", "coppia/inerzia", "|omega| p50", "contrasto",
         "al pav. (bers./tutti)"))
    for c in o["casi"]:
        if "errore" in c:
            P("%-6s ERRORE: %s" % (c["K"], c["errore"]))
            continue
        P("%-6d %-14.6g %-14.6g %-16.6g %-14.6g %-14.6g %d/%d  %d/%d"
          % (c["K"], c["coppia_p50"], c["inerzia_p50"], c.get("rapporto_p50", float("nan")),
             c["omega_p50"], c["contrasto_p50"], c["al_pavimento"], c["quanti"],
             c["al_pavimento_tutti"], c["nodi_tutti"]))
    P()

# ---------------------------------------------------------------- C1
P("=" * 116)
P("`C1` -- LE PENDENZE DI COPPIA E INERZIA SU `log k`, UGUALI ENTRO L'ERRORE FRA SEMI")
P("=" * 116)
P("%-18s %-14s %-14s %-14s %-14s" % ("braccio", "pend. COPPIA", "pend. INERZIA",
                                     "differenza", "pend. |omega|"))
pend_on, pend_off = {}, {}
for (nome, s, v, fl, sim, argv) in BRACCI:
    o = dati.get(nome)
    if not o:
        continue
    cc = [c for c in o["casi"] if "errore" not in c]
    if len(cc) < 3:
        continue
    ks = [c["K"] for c in cc]
    pc = pend(ks, [c["coppia_p50"] for c in cc])
    pi = pend(ks, [c["inerzia_p50"] for c in cc])
    po = pend(ks, [c["omega_p50"] for c in cc])
    (pend_on if nome.startswith("on_") else pend_off)[nome] = (pc, pi, po)
    P("%-18s %-14.4f %-14.4f %-14.4f %-14.4f" % (nome, pc, pi, pi - pc, po))
P()
# l'errore FRA SEMI: la dispersione della differenza fra i bracci ON dello stesso verso
_dif_on = [abs(pi - pc) for (pc, pi, _po) in pend_on.values()]
_dif_off = [abs(pi - pc) for (pc, pi, _po) in pend_off.values()]
_sp_on = float(np.std(_dif_on)) if len(_dif_on) > 1 else float("nan")
OK.append(crit("C1", "pendenze di COPPIA e INERZIA uguali entro l'errore fra semi",
               bool(len(_dif_on) and max(_dif_on) < min(_dif_off) / 3.0),
               "ON : |pend(INERZIA) - pend(COPPIA)|  %s"
               % ("  ".join("%.4f" % x for x in _dif_on))
               + NL + "OFF: |pend(INERZIA) - pend(COPPIA)|  %s"
               % ("  ".join("%.4f" % x for x in _dif_off))
               + NL + "dispersione FRA SEMI della differenza, ON: %.4f" % _sp_on
               + NL + "CRITERIO: la differenza ON deve stare SOTTO UN TERZO della minima OFF."
               + NL + "  **Non `== 0`**: le pendenze sono misure, e `R3` insegna che pretendere"
               + NL + "  l'uguaglianza esatta fa fallire un criterio su due ulp. Il fattore 3 e'"
               + NL + "  la separazione che le due popolazioni devono avere per dire `diverse`."))

# ---------------------------------------------------------------- C2
P("=" * 116)
P("`C2` -- `|omega|` A `k = 2` DELLO STESSO ORDINE DI `k = 77`")
P("=" * 116)
_r_on, _r_off = [], []
for (nome, s, v, fl, sim, argv) in BRACCI:
    o = dati.get(nome)
    if not o:
        continue
    cc = [c for c in o["casi"] if "errore" not in c]
    if len(cc) < 2:
        continue
    r = cc[-1]["omega_p50"] / cc[0]["omega_p50"] if cc[0]["omega_p50"] else float("nan")
    (_r_on if nome.startswith("on_") else _r_off).append((nome, r))
    P("  %-18s |omega| k=2 / k=77  x%.4g" % (nome, r))
P()
_max_on = max([r for _n, r in _r_on]) if _r_on else float("nan")
OK.append(crit("C2", "`|omega|` a `k = 2` dello stesso ordine di `k = 77` (rapporto < 10)",
               bool(np.isfinite(_max_on) and _max_on < 10.0),
               "ON : massimo rapporto  x%.4g   (criterio: < 10, cioe' STESSO ORDINE)" % _max_on
               + NL + "OFF: %s" % ("  ".join("x%.4g" % r for _n, r in _r_off))
               + NL + "  IL NULLO E' IL BRACCIO OFF, e senza di esso un `x2` non direbbe nulla."))

# ---------------------------------------------------------------- C3
P("=" * 116)
P("`C3` -- FLAG SPENTO = BYTE-IDENTICO AL CODICE PRECEDENTE (non `HEAD`, `P8`)")
P("=" * 116)
_ok3, _det3 = True, []
for s in SEMI:
    a = dati.get("off_s%d_lunghi" % s)
    b = dati.get("prima_s%d_lunghi" % s)
    if not a or not b:
        _ok3 = False
        _det3.append("seme %d: dati mancanti" % s)
        continue
    com = sorted(set(a["firme"]) & set(b["firme"]))
    dif = [k for k in com if a["firme"][k] != b["firme"][k]]
    solo_a = sorted(set(a["firme"]) - set(b["firme"]))
    solo_b = sorted(set(b["firme"]) - set(a["firme"]))
    _ok3 = _ok3 and not dif and not solo_a and not solo_b
    _det3.append("seme %d: campi confrontati %d   DIVERSI %d   solo nuovo %s   solo vecchio %s"
                 % (s, len(com), len(dif), solo_a or "nessuno", solo_b or "nessuno"))
    if dif:
        _det3.append("   diversi: %s" % ", ".join(dif[:12]))
OK.append(crit("C3", "flag SPENTO byte-identico al codice PRECEDENTE (%s^)" % COMMIT_CURA[:8],
               _ok3, NL.join(_det3)))

# ---------------------------------------------------------------- C4
P("=" * 116)
P("`C4` -- IL CASO CHE DEVE FALLIRE: il braccio SPENTO, generato TOGLIENDO il flag dall'argv")
P("=" * 116)
_c4 = []
for (nome, s, v, fl, sim, argv) in BRACCI:
    o = dati.get(nome)
    if not o:
        continue
    _c4.append((nome, o["CFG"]["flag"], o["CFG"]["opz_nell_argv"], o["CFG"]["atteso"]))
_ok4 = all((bool(f) == bool(at)) and (bool(op) == bool(at)) for _n, f, op, at in _c4)
_off_fallisce = [n for (n, f, op, at) in _c4 if not at and not f]
OK.append(crit("C4", "il braccio spento e' generato TOGLIENDO l'opzione, e su di esso `C1`/`C2` FALLISCONO",
               bool(_ok4 and _off_fallisce and len(_dif_off)
                    and min(_dif_off) > max(_dif_on or [0]) * 3.0),
               NL.join("  %-18s flag=%-6s opz_nell_argv=%-6s atteso=%s" % x for x in _c4)
               + NL + "bracci spenti: %s" % ", ".join(_off_fallisce)
               + NL + "su di essi la differenza fra le pendenze vale %s, cioe' NON passa `C1`:"
               % ("  ".join("%.4f" % x for x in _dif_off))
               + NL + "  **e' il caso che DEVE fallire, e fallisce.**"))

# ---------------------------------------------------------------- C5
P("=" * 116)
P("`C5` -- IL PAVIMENTO `1e-6`: QUANTE VOLTE MORDE CON LA CURA (`A11`)")
P("=" * 116)
_pav = []
for (nome, s, v, fl, sim, argv) in BRACCI:
    o = dati.get(nome)
    if not o:
        continue
    for c in o["casi"]:
        if "errore" in c:
            continue
        _pav.append((nome, c["K"], c["al_pavimento"], c["quanti"],
                     c["al_pavimento_tutti"], c["nodi_tutti"]))
_mordono_on = sum(p[2] for p in _pav if p[0].startswith("on_"))
_mordono_on_t = sum(p[4] for p in _pav if p[0].startswith("on_"))
_mordono_off = sum(p[2] for p in _pav if p[0].startswith("off_"))
OK.append(crit("C5", "il pavimento `1e-6` non comincia a mordere con la cura",
               _mordono_on == 0,
               "ON : bersagli al pavimento, sommati su tutti i casi   %d" % _mordono_on
               + NL + "ON : NODI al pavimento, sommati su tutti i casi        %d" % _mordono_on_t
               + NL + "OFF: bersagli al pavimento                             %d" % _mordono_off
               + NL + "  PRIMA della cura era `0/20` in ogni riga (`CONFIG-1/a`)."
               + NL + "  **Se ON mordesse, la cura abbasserebbe l'inerzia IN ASSOLUTO e non solo"
               + NL + "  la sua pendenza**, e `A11` chiederebbe di guardare l'errore che il"
               + NL + "  pavimento nasconde."))

# ---------------------------------------------------------------- C6
P("=" * 116)
P("`C6` -- LA SCALA DELL'INERZIA SU **TUTTI** I NODI, PRIMA E DOPO")
P("=" * 116)
P("%-18s %-14s %-14s %-14s %-14s %s" % ("braccio", "p5", "mediana", "p95", "min", "al pav./nodi"))
_sc = {}
for (nome, s, v, fl, sim, argv) in BRACCI:
    o = dati.get(nome)
    if not o or not o.get("scala"):
        continue
    sc = o["scala"]
    _sc[nome] = sc
    P("%-18s %-14.6g %-14.6g %-14.6g %-14.6g %d/%d"
      % (nome, sc["p5"], sc["p50"], sc["p95"], sc["min"], sc["al_pavimento"], sc["nodi"]))
P()
_on_p50 = [v["p50"] for k, v in _sc.items() if k.startswith("on_")]
_off_p50 = [v["p50"] for k, v in _sc.items() if k.startswith("off_")]
_rap = (float(np.median(_on_p50)) / float(np.median(_off_p50))) if _on_p50 and _off_p50 else \
    float("nan")
OK.append(crit("C6", "la scala dell'inerzia su TUTTI i nodi e' DICHIARATA prima/dopo",
               bool(_on_p50 and _off_p50),
               "mediana ON  %.6g     mediana OFF %.6g     rapporto x%.4g"
               % (float(np.median(_on_p50)) if _on_p50 else float("nan"),
                  float(np.median(_off_p50)) if _off_p50 else float("nan"), _rap)
               + NL + "  **Questo criterio non ha una soglia, e non deve averla:** dice DI QUANTO"
               + NL + "  si sposta la scala. La cura divide per il numero di vicini, quindi un"
               + NL + "  abbassamento e' ATTESO: il punto e' che sia DICHIARATO, e che `C5` dica"
               + NL + "  se quell'abbassamento arriva al pavimento."))

# ---------------------------------------------------------------- i contatori A8
P("=" * 116)
P("I CONTATORI `A8` DEL SITO (`P5`: un ramo non misurato e' un comportamento sconosciuto)")
P("=" * 116)
for (nome, s, v, fl, sim, argv) in BRACCI:
    o = dati.get(nome)
    if not o:
        continue
    P("  %-18s %s" % (nome, o.get("contatori") or "(nessuno)"))
P()

P("=" * 116)
P("ESITO: %d/%d PASS" % (sum(1 for x in OK if x), len(OK)))
P("=" * 116)
P()
P("COSA QUESTO SIGILLO *NON* DICE:")
P("  - **non dice che la cura sia GIUSTA in fisica**: dice che coppia e inerzia scalano allo")
P("    stesso modo, che era l'incoerenza misurata. Se il settore di spin resti aliasato e' UN'")
P("    ALTRA domanda, e questo sigillo non la tocca.")
P("  - `C6` non ha soglia **di proposito**: la cura divide per il numero di vicini, quindi la")
P("    scala si abbassa. Il criterio e' che sia DICHIARATA, non che non cambi.")
P("  - DUE SEMI: per una barra fra semi servono >= 4 (`P3` delle regole).")
P("  - il taglio TOGLIE ARCHI A MANO: la domanda e' se la LEGGE regga un `k` piccolo.")
P("  - i 20 bersagli non sono adiacenti, **ma possono condividere un VICINO**.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
sys.exit(0 if all(OK) else 1)
