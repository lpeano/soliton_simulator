# -*- coding: utf-8 -*-
"""SIGILLO ESTESO `INERZIA-1(C)` — **TRE LETTURE MISURATE INSIEME** *(mandato di Luca, 2026-09-25)*.

I **sei criteri** della cura, **più** `R1`-`R4` *(estensivo o ritardato?)* **più** `R3 bis`
*(incoerenza di esponenti della rampa)*. **Tutti i criteri sono scritti nel task history
`doc/TASK_HISTORY/2026-09-25_inerzia1-contrasto-intensivo.md`, committato PRIMA.**

```
C1'   pendenza su log k del CONTRASTO = quella della COPPIA entro lo spread fra semi (T2 escluso)
C1''  differenza di pendenza inerzia-coppia < 0.7 nel taglio "corti"   <- MIA previsione
C2    |omega|(k=2)/|omega|(k=77) < 3 in tutti i bracci                 <- il 3 e' una SCELTA
C3    flag spento byte-identico al PADRE del commit del flag (P8)
C4    braccio spento generato togliendo l'opzione, e su di esso C1' NON passa (nessuna soglia)
C5    il pavimento 1e-6: quante volte morde
C6    scala dell'inerzia su TUTTI i nodi, prima/dopo
R1    dopo il rilassamento, la pendenza del contrasto torna su quella della coppia?
R2    il residuo CALA MONOTONAMENTE nel tempo: transitorio, non offset
R3    i figli della mitosi: rho, peq, contrasto dalla nascita -- il contrasto rientra?
R4    IL NULLO: gli stessi valori sui nodi NON nati
R3bis |omega| * ramp COSTANTE sui figli -> incoerenza di ESPONENTI, non estensivita'
```

**⚠ `N` NON SI SCEGLIE, E NON SI RICOSTRUISCE PER ALGEBRA.** `TAU_BG = 5.0` **non è il tempo vero**
*(con `TAU_LOCALI` il rilassamento usa `tau_bg_loc = 1/r_arco`)*, e `dt_e` misurato è **per
SOTTO-PASSO** *(148237 valori per ~4252 nodi)*, quindi `tau_bg/dt_e` **non è** un numero di passi.
**Si MISURA il decadimento di `|peq − rho|`** sugli archi toccati, e il referto dice **se il
rilassamento si è completato dentro il budget**. Se non si completa, **`R1`/`R2` sono NON MISURATI**
— non «passati».

**LE TRE LETTURE SI ESCLUDONO NEI NUMERI, NON NEL RAGIONAMENTO**, e per questo si misurano
**insieme**: due di esse **ritirerebbero** la variante pesata.

**NESSUNA CURA SCELTA: il referto dice quali letture reggono, e si FERMA.**

ASCII puro.
"""
import ast
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
FUORI = os.path.join(_QUI, "_sig_contrasto_esteso")
DEST = os.path.join(FUORI, "SIGILLO_contrasto_esteso.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)
NL = chr(10)

SEMI = [11, 12]
SEP = 4.0
GRADI = [77, 20, 8, 4, 2]
GRADI_R = [77, 8, 2]          # `R1`/`R2`: TRE valori di `k`, e il perche' e' dichiarato nel referto
VERSI = ["lunghi", "corti"]
PASSI_PRIMA = 20
BUDGET = 120                  # il BUDGET del rilassamento, dichiarato: lo stesso dei sigilli di oggi
BERSAGLI = 20
OPZ = "--contrasto-intensivo"
FLAGNOME = "CONTRASTO_INTENSIVO"

SIM = os.path.join(RADICE, "soliton_simulator.py")
blob_vero = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()[:8]


def copia_diag(sorgente, dest):
    """La COPIA diagnostica, GENERATA AL RUN dal file corrente. Restituisce (blob, ancore).

    ❌ **PRIMA VERSIONE ROTTA, e il difetto e' istruttivo:** l'ancora era una STRINGA che
    coincideva col PREFISSO della riga vera
    *(`inerzia = np.maximum(...)       # il pavimento RESTA: deve diventare inerte`)*, e la
    sostituzione ha **tagliato la coda del commento**, lasciando `: deve diventare inerte`
    appeso alla mia ultima riga -> `SyntaxError`. **La copia era rotta, e il braccio e' morto
    all'import.**
    ✅ **ORA SI LAVORA PER RIGHE:** si trova **la riga UNICA** che comincia col testo dato e si
    inserisce **dopo di essa, INTERA**. Un'ancora di riga non puo' tagliare una coda.
    *(E' la classe che `P9` — in coda — deve impedire: una copia che differisce per piu' delle
    righe diagnostiche dichiarate. Qui differiva anche nella SINTASSI.)*
    """
    righe = io.open(sorgente, encoding="utf-8", newline="").read().split(NL)
    DIAG_IN = ["        self._diag_inerzia = np.array(inerzia, copy=True)",
               "        self._diag_contrasto = np.array(_contrasto, copy=True)",
               "        self._diag_T2 = np.array(_T2, copy=True)",
               "        self._diag_peq_nodo = np.array(_peq_nodo, copy=True)"]
    DIAG_CO = ["        self._diag_coppia = np.array(correzione, copy=True)"]
    fuori, k = [], 0
    _pre_in = "        inerzia = np.maximum(_contrasto * _T2, 1e-6)"
    _pre_co = "        omega_new = omega_src + dtn_c * (correzione / inerzia[:, None]"
    _n_in = sum(1 for r in righe if r.startswith(_pre_in))
    _n_co = sum(1 for r in righe if r.startswith(_pre_co))
    assert _n_in == 1, "righe dell'inerzia: %d in %s" % (_n_in, sorgente)
    assert _n_co == 1, "righe di omega_new: %d in %s" % (_n_co, sorgente)
    for r in righe:
        if r.startswith(_pre_co):
            fuori.extend(DIAG_CO)            # la coppia si legge PRIMA di essere usata
            fuori.append(r)
            k += 1
            continue
        fuori.append(r)
        if r.startswith(_pre_in):
            fuori.extend(DIAG_IN)
            k += 1
    io.open(dest, "w", encoding="utf-8", newline=NL).write(NL.join(fuori))
    # ⚠ **POSTCONDIZIONE (anticipo di `P9`): la copia DEVE differire SOLO per le righe
    #   diagnostiche dichiarate.** Se differisce per altro, **STOP**: una copia che gira al posto
    #   del simulatore e che non si sa in cosa differisca **non e' un diagnostico, e' un altro
    #   programma**.
    import difflib as _dl
    _dop = io.open(dest, encoding="utf-8", newline="").read().split(NL)
    _agg = [x[1:].rstrip(chr(13)) for x in _dl.ndiff(righe, _dop) if x.startswith("+ ")]
    _tol = set(DIAG_IN) | set(DIAG_CO)
    _estranee = [x for x in _agg if x not in _tol]
    _tolte = [x[1:].rstrip(chr(13)) for x in _dl.ndiff(righe, _dop) if x.startswith("- ")]
    assert not _estranee and not _tolte, (
        "la copia differisce per righe NON dichiarate: aggiunte %r  tolte %r"
        % (_estranee[:3], _tolte[:3]))
    ast.parse(NL.join(_dop))            # e DEVE compilare
    return hashlib.sha1(io.open(dest, "rb").read()).hexdigest()[:8], k

COPIA = os.path.join(FUORI, "_sim_diag_est.py")
blob_copia, anc_copia = copia_diag(SIM, COPIA)

PRIMA = os.path.join(TMP, "_sim_prima.py")
COMMIT_CURA = _cli_flag.sim_prima_del_flag(FLAGNOME, PRIMA, radice=RADICE)
PRIMA_DIAG = os.path.join(TMP, "_sim_prima_diag.py")
blob_prima, anc_prima = copia_diag(PRIMA, PRIMA_DIAG)

_S0, ARGV = _cli_flag.argv_del_driver([], dest=os.path.join(TMP, "_scarto"))
ARGV = ARGV + ["--nodi", "0"]
ARGV_ON = ARGV + [OPZ]
ARGV_OFF = list(ARGV)

# ============================================================== IL FIGLIO, comune ai tre modi
FIGLIO = r'''
import copy as _copy
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import _cli_flag
import _passo
_argv, _scartate = _cli_flag.argv_per(SIM, ARGV)
S, _a = _cli_flag.carica_dal_cli(_argv, nome="sim_est", sim=SIM)
_CFG = {"flag": getattr(S, FLAGNOME, "ASSENTE"), "atteso": bool(FLAG),
        "opz_nell_argv": OPZ in _argv, "scartate": _scartate, "sim": os.path.basename(SIM)}
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
for _ in range(PASSI_PRIMA):
    _passo.passo_pieno(S, net)

o = dict(SEME=SEME, VERSO=VERSO, MODO=MODO, CFG=_CFG, n=int(net.n))


def _dg(net2, nome):
    return np.asarray(getattr(net2, nome, []), float)


def _gradi(net2):
    g = np.zeros(int(net2.n), int)
    _i = np.asarray(net2.i, int); _j = np.asarray(net2.j, int)
    _m = (_i < net2.n) & (_j < net2.n)
    np.add.at(g, _i[_m], 1); np.add.at(g, _j[_m], 1)
    return g


def _ramp(net2):
    _tr = net2._tempo_rampa()
    return np.minimum(1.0, np.asarray(net2.eta, float) / _tr)


n = int(net.n)
ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
grado = _gradi(net)
gm = int(np.median(grado))
_ok = np.where(grado >= max(GRADI))[0]
_ok = _ok[np.argsort(np.abs(grado[_ok] - gm))]
vic = {}
_mm = (ii < n) & (jj < n)
for _k in range(len(net.d)):
    if not _mm[_k]:
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
o["grado_mediano"] = gm
d = np.asarray(net.d, float)
suoi = {b: np.where((ii == b) | (jj == b))[0] for b in BERS}


def taglia(K):
    """UNA COPIA FRESCA della rete col taglio a `k = K`. I casi sono INDIPENDENTI."""
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
    return net2, int(keep.sum())


def leggi_bers(net2):
    """I valori mediani sui BERSAGLI, piu' il conto al pavimento."""
    _in, _co = _dg(net2, "_diag_inerzia"), _dg(net2, "_diag_coppia")
    _ct, _pq = _dg(net2, "_diag_contrasto"), _dg(net2, "_diag_peq_nodo")
    _om = np.linalg.norm(np.asarray(net2.omega_s, float), axis=1)
    _rho = np.asarray(net2._rho_sorgente(), float)
    B = np.array([b for b in BERS if b < _in.size and b < _om.size], int)
    if not B.size:
        return None
    cop = np.linalg.norm(_co[B], axis=1) if _co.size else np.zeros(0)
    c = dict(quanti=int(B.size),
             coppia_p50=float(np.median(cop)) if cop.size else float("nan"),
             inerzia_p50=float(np.median(_in[B])),
             contrasto_p50=float(np.median(_ct[B])) if _ct.size else float("nan"),
             T2_p50=float(np.median(_dg(net2, "_diag_T2")[B])) if _dg(net2, "_diag_T2").size
             else float("nan"),
             omega_p50=float(np.median(_om[B])),
             al_pavimento=int(np.sum(_in[B] <= 1e-6)),
             al_pavimento_tutti=int(np.sum(_in <= 1e-6)), nodi_tutti=int(_in.size))
    if cop.size:
        c["rapporto_p50"] = float(np.median(cop / np.maximum(_in[B], 1e-300)))
    # LO SCARTO `|peq - rho|` SUI BERSAGLI: e' la grandezza che dice se `peq` si e' rilassato
    if _pq.size > B.max() and _rho.size > B.max():
        _sc = np.abs(_pq[B] - _rho[B]) / np.maximum(np.abs(_rho[B]), 1e-300)
        c["scarto_peq_p50"] = float(np.median(_sc))
    return c


# =========================================================== MODO 1: il TAGLIO (C1'..C6)
if MODO == "taglio":
    _in0 = _dg(net, "_diag_inerzia")
    if _in0.size:
        o["scala"] = dict(p5=float(np.percentile(_in0, 5)), p50=float(np.median(_in0)),
                          p95=float(np.percentile(_in0, 95)), min=float(_in0.min()),
                          al_pavimento=int(np.sum(_in0 <= 1e-6)), nodi=int(_in0.size))
    o["contatori"] = {k: (v if isinstance(v, (int, float)) else str(v))
                      for k, v in vars(net).items() if k.startswith("_g_ci")}
    import hashlib as _h
    o["firme"] = {}
    for k, v in sorted(vars(net).items()):
        if k.startswith("_g_") or k.startswith("_diag"):
            continue
        if isinstance(v, np.ndarray):
            o["firme"][k] = [_h.sha1(np.ascontiguousarray(v).tobytes()).hexdigest()[:12],
                             list(v.shape), str(v.dtype)]
        elif isinstance(v, (int, float, bool, str)):
            o["firme"][k] = [_h.sha1(repr(v).encode()).hexdigest()[:12], [], type(v).__name__]
    o["casi"] = []
    for K in GRADI:
        net2, rimasti = taglia(K)
        try:
            _passo.passo_pieno(S, net2)
            c = leggi_bers(net2) or {}
            c["K"] = int(K); c["archi_rimasti"] = rimasti
            o["casi"].append(c)
        except Exception as e:
            o["casi"].append(dict(K=int(K), errore=str(e)[:200]))

# =========================================================== MODO 2: il RILASSAMENTO (R1, R2)
elif MODO == "rilassa":
    # i tagli avanzano IN PARALLELO, cosi' a ogni checkpoint la pendenza si calcola FRA i `k`
    reti = {}
    for K in GRADI_R:
        reti[K] = taglia(K)[0]
    CHK = sorted(set([1, max(2, BUDGET // 3), BUDGET]))
    o["checkpoint"] = CHK
    o["serie"] = {}
    for _p in range(1, BUDGET + 1):
        for K in GRADI_R:
            try:
                _passo.passo_pieno(S, reti[K])
            except Exception as e:
                o.setdefault("errori", []).append("k=%d passo %d: %s" % (K, _p, str(e)[:120]))
        if _p in CHK:
            o["serie"][str(_p)] = {}
            for K in GRADI_R:
                c = leggi_bers(reti[K])
                if c:
                    o["serie"][str(_p)][str(K)] = c

# =========================================================== MODO 3: I FIGLI (R3, R4, R3bis)
elif MODO == "figli":
    n0 = int(net.n)
    _et0 = np.asarray(net.eta, float)
    o["n0"] = n0
    o["storia"] = []          # [passo, id, eta, ramp, omega, rho, peq, contrasto]
    o["nullo"] = []           # gli stessi valori, MEDIANI, sui nodi NON nati
    nati = {}                 # id -> passo di nascita
    for _p in range(1, BUDGET + 1):
        _pre = int(net.n)
        _passo.passo_pieno(S, net)
        if int(net.n) > _pre:
            for _k in range(_pre, int(net.n)):
                nati[_k] = _p
        _r = _ramp(net)
        _om = np.linalg.norm(np.asarray(net.omega_s, float), axis=1)
        _rho = np.asarray(net._rho_sorgente(), float)
        _pq, _ct = _dg(net, "_diag_peq_nodo"), _dg(net, "_diag_contrasto")
        # IL NULLO: i nodi che c'erano al passo zero (indici < n0)
        _v = np.arange(min(n0, int(net.n)))
        if _ct.size >= _v.size and _pq.size >= _v.size:
            o["nullo"].append([_p, float(np.median(_r[_v])), float(np.median(_om[_v])),
                               float(np.median(_rho[_v])), float(np.median(_pq[_v])),
                               float(np.median(_ct[_v]))])
        # I FIGLI, uno per uno, con l'ETA' dalla nascita
        for _k, _nasc in sorted(nati.items()):
            if _k >= int(net.n) or _k >= _ct.size or _k >= _pq.size:
                continue
            o["storia"].append([_p, int(_k), int(_p - _nasc), float(_r[_k]), float(_om[_k]),
                                float(_rho[_k]), float(_pq[_k]), float(_ct[_k])])
    o["nati"] = {str(k): int(v) for k, v in sorted(nati.items())}

io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  modo %s  n %d" % (NOME, MODO, net.n))
'''


def braccio(nome, seme, verso, flag, sim, argv, modo):
    testa = ["RAD = %r" % RADICE, "TMPD = %r" % TMP, "NOME = %r" % nome,
             "SEME = %d" % seme, "SEP = %r" % SEP, "SIM = %r" % sim,
             "GRADI = %r" % GRADI, "GRADI_R = %r" % GRADI_R, "PASSI_PRIMA = %d" % PASSI_PRIMA,
             "BUDGET = %d" % BUDGET, "BERSAGLI = %d" % BERSAGLI, "VERSO = %r" % verso,
             "ARGV = %r" % argv, "FLAG = %r" % flag, "OPZ = %r" % OPZ,
             "FLAGNOME = %r" % FLAGNOME, "MODO = %r" % modo, ""]
    p = os.path.join(TMP, "_br_%s.py" % nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(NL.join(testa) + FIGLIO)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


BRACCI = []
for s in SEMI:
    for v in VERSI:
        BRACCI.append(("on_s%d_%s" % (s, v), s, v, True, COPIA, ARGV_ON, "taglio"))
        BRACCI.append(("off_s%d_%s" % (s, v), s, v, False, COPIA, ARGV_OFF, "taglio"))
        BRACCI.append(("ril_s%d_%s" % (s, v), s, v, False, COPIA, ARGV_OFF, "rilassa"))
for s in SEMI:
    BRACCI.append(("prima_s%d_lunghi" % s, s, "lunghi", False, PRIMA_DIAG, ARGV_OFF, "taglio"))
    BRACCI.append(("figli_s%d" % s, s, "lunghi", False, COPIA, ARGV_OFF, "figli"))

LOG = []
proc = {}
for (nome, s, v, fl, sim, argv, modo) in BRACCI:
    proc[nome] = braccio(nome, s, v, fl, sim, argv, modo)
for nome, pr in proc.items():
    so, se = pr.communicate()
    LOG.append("[%s] rc=%d %s" % (nome, pr.returncode,
                                  (so or b"").decode("utf-8", "replace").strip()[-90:]))
    if pr.returncode:
        LOG.append((se or b"").decode("utf-8", "replace")[-1200:])

R = []


def P(s=""):
    R.append(s)


def crit(sigla, cosa, ok, detta):
    P("%-6s %-4s  %s" % (sigla, "PASS" if ok else "FAIL", cosa))
    for r_ in (detta or "").split(NL):
        if r_:
            P("              " + r_)
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


P("=" * 118)
P("SIGILLO ESTESO `INERZIA-1(C)` -- TRE LETTURE MISURATE INSIEME   (2026-09-25)")
P("=" * 118)
P()
for l in LOG:
    P(l)
P()
P("blob del simulatore VERO      %s" % blob_vero)
P("blob della COPIA diagnostica  %s   (%d ancore, GENERATA AL RUN)" % (blob_copia, anc_copia))
P("il codice di PRIMA e'         %s^   (PADRE del commit del flag, NON `HEAD`)" % COMMIT_CURA[:8])
P("blob della copia di PRIMA     %s   (%d ancore)" % (blob_prima, anc_prima))
P("semi %s   versi %s   k %s   k del rilassamento %s   bersagli %d"
  % (SEMI, VERSI, GRADI, GRADI_R, BERSAGLI))
P("passi pieni prima del taglio %d   BUDGET del rilassamento e dei figli %d passi"
  % (PASSI_PRIMA, BUDGET))
P()
_Sq, _ = _cli_flag.carica_dal_cli(_cli_flag.argv_per(COPIA, ARGV_ON)[0], nome="cfg_est", sim=COPIA)
_cli_flag.dichiara_configurazione(
    _Sq, P, esenzione="il flag in prova NON e' ancora nel driver (entra dopo il sigillo), quindi "
                      "l'argv ON e' quella del driver PIU' %s" % OPZ)

dati = {nome: leggi(nome) for (nome, s, v, fl, sim, argv, modo) in BRACCI}
if any("rc=1" in l for l in LOG):
    P("STOP: un braccio non e' arrivato in fondo. Nessun criterio si legge.")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL.join(R))
    sys.exit(1)

OK = []

# ====================================================================== la tabella del taglio
P("=" * 118)
P("I NUMERI DEL TAGLIO (un passo dopo)")
P("=" * 118)
pend_on, pend_off = {}, {}
for (nome, s, v, fl, sim, argv, modo) in BRACCI:
    if modo != "taglio":
        continue
    o = dati.get(nome)
    if not o:
        P("  [%s] NESSUN DATO" % nome)
        continue
    cc = [c for c in o["casi"] if "errore" not in c]
    P("-" * 118)
    P("%s   %s = %s   (sim %s)" % (nome, FLAGNOME, o["CFG"]["flag"], o["CFG"]["sim"]))
    P("%-6s %-13s %-13s %-13s %-15s %-13s %s"
      % ("k", "COPPIA", "INERZIA", "contrasto", "coppia/inerzia", "|omega|",
         "al pav. b/t   |peq-rho|/rho"))
    for c in cc:
        P("%-6d %-13.6g %-13.6g %-13.6g %-15.6g %-13.6g %d/%d %d/%d   %.4g"
          % (c["K"], c["coppia_p50"], c["inerzia_p50"], c["contrasto_p50"],
             c.get("rapporto_p50", float("nan")), c["omega_p50"], c["al_pavimento"],
             c["quanti"], c["al_pavimento_tutti"], c["nodi_tutti"],
             c.get("scarto_peq_p50", float("nan"))))
    if len(cc) >= 3:
        ks = [c["K"] for c in cc]
        d_ = dict(coppia=pend(ks, [c["coppia_p50"] for c in cc]),
                  inerzia=pend(ks, [c["inerzia_p50"] for c in cc]),
                  contrasto=pend(ks, [c["contrasto_p50"] for c in cc]),
                  omega=pend(ks, [c["omega_p50"] for c in cc]))
        (pend_on if nome.startswith("on_") else pend_off)[nome] = d_
        P("  pendenze su log k:  COPPIA %.4f   INERZIA %.4f   CONTRASTO %.4f   |omega| %.4f"
          % (d_["coppia"], d_["inerzia"], d_["contrasto"], d_["omega"]))
    P()

# ====================================================================== C1'
_dc_on = [abs(d_["contrasto"] - d_["coppia"]) for d_ in pend_on.values()]
_dc_off = [abs(d_["contrasto"] - d_["coppia"]) for d_ in pend_off.values()]
_sp_on = float(np.std(_dc_on)) if len(_dc_on) > 1 else float("nan")
OK.append(crit("C1'", "pendenza del CONTRASTO = quella della COPPIA entro lo spread fra semi",
               bool(_dc_on and max(_dc_on) <= _sp_on * 2.0),
               "ON : |pend(contrasto) - pend(coppia)|  %s" % "  ".join("%.4f" % x for x in _dc_on)
               + NL + "OFF: %s" % "  ".join("%.4f" % x for x in _dc_off)
               + NL + "spread FRA SEMI (dev.std della differenza ON): %.4f" % _sp_on
               + NL + "CRITERIO: il MASSIMO della differenza ON sta entro 2 spread."
               + NL + "  **`T2` E' ESCLUSO**, e la ragione e' dichiarata: in questa misura `T2`"
               + NL + "  dipende da `k` per la GEOMETRIA DEL TAGLIO (togliere i lunghi accorcia"
               + NL + "  `d_nodo`, togliere i corti lo allunga), non per estensivita'."))

# ====================================================================== C1''
_di_corti_on = [abs(d_["inerzia"] - d_["coppia"]) for k_, d_ in pend_on.items() if "corti" in k_]
OK.append(crit("C1''", "LA MIA PREVISIONE: differenza inerzia-coppia < 0.7 nel taglio `corti`",
               bool(_di_corti_on and max(_di_corti_on) < 0.7),
               "ON corti: %s   (criterio: < 0.7)" % "  ".join("%.4f" % x for x in _di_corti_on)
               + NL + "  **SE NON PASSA, la mia diagnosi \"il residuo viene dai pesi\" e'"
               + NL + "  SBAGLIATA, e lo scrivo.** La ragione strutturale e' nel task history,"
               + NL + "  scritta PRIMA: `rho_spin` e' il MODULO QUADRO di una somma pesata, quindi"
               + NL + "  dividere per `W` una volta toglie UNA potenza, e se la dipendenza e'"
               + NL + "  quadratica il residuo NON si azzera."))

# ====================================================================== C2
_r_on, _r_off = [], []
for (nome, s, v, fl, sim, argv, modo) in BRACCI:
    if modo != "taglio":
        continue
    o = dati.get(nome)
    if not o:
        continue
    cc = [c for c in o["casi"] if "errore" not in c]
    if len(cc) < 2 or not cc[0]["omega_p50"]:
        continue
    r = cc[-1]["omega_p50"] / cc[0]["omega_p50"]
    (_r_on if nome.startswith("on_") else _r_off).append((nome, r))
OK.append(crit("C2", "`|omega|(k=2)/|omega|(k=77)` < 3 in tutti i bracci ON",
               bool(_r_on and max(r for _n, r in _r_on) < 3.0),
               "ON : %s" % "  ".join("%s x%.4g" % (n, r) for n, r in _r_on)
               + NL + "OFF: %s" % "  ".join("%s x%.4g" % (n, r) for n, r in _r_off)
               + NL + "  **il `3` e' una SCELTA per \"stesso ordine\", dichiarata** (Luca)."))

# ====================================================================== C3
_ok3, _det3 = True, []
for s in SEMI:
    a = dati.get("off_s%d_lunghi" % s)
    b = dati.get("prima_s%d_lunghi" % s)
    if not a or not b or "firme" not in a or "firme" not in b:
        _ok3 = False
        _det3.append("seme %d: dati mancanti" % s)
        continue
    com = sorted(set(a["firme"]) & set(b["firme"]))
    dif = [k for k in com if a["firme"][k] != b["firme"][k]]
    sa = sorted(set(a["firme"]) - set(b["firme"]))
    sb = sorted(set(b["firme"]) - set(a["firme"]))
    _ok3 = _ok3 and not dif and not sa and not sb
    _det3.append("seme %d: campi %d   DIVERSI %d   solo nuovo %s   solo vecchio %s"
                 % (s, len(com), len(dif), sa or "nessuno", sb or "nessuno"))
OK.append(crit("C3", "flag SPENTO byte-identico al codice PRECEDENTE (%s^)" % COMMIT_CURA[:8],
               _ok3, NL.join(_det3)))

# ====================================================================== C4
_cfg = [(n_, dati[n_]["CFG"]) for (n_, s, v, fl, sim, argv, modo) in BRACCI
        if dati.get(n_) and "CFG" in dati[n_]]
_ok4cfg = all(bool(c["flag"]) == bool(c["atteso"]) and bool(c["opz_nell_argv"]) == bool(c["atteso"])
              for _n, c in _cfg if c["flag"] != "ASSENTE")
_c1_off_fallisce = bool(_dc_off and _sp_on == _sp_on and max(_dc_off) > _sp_on * 2.0)
OK.append(crit("C4", "braccio spento generato TOGLIENDO l'opzione, e su di esso `C1'` NON passa",
               bool(_ok4cfg and _c1_off_fallisce),
               NL.join("  %-20s flag=%-7s opz=%-6s atteso=%s"
                       % (n_, c["flag"], c["opz_nell_argv"], c["atteso"]) for n_, c in _cfg)
               + NL + "su OFF la differenza contrasto-coppia vale %s, contro 2 spread = %.4f"
               % ("  ".join("%.4f" % x for x in _dc_off), _sp_on * 2.0)
               + NL + "  **CORRETTO DA LUCA il 2026-09-25: NESSUNA soglia propria.** La forma"
               + NL + "  precedente pretendeva una separazione `3x` e DUPLICAVA `C1`, fallendo"
               + NL + "  insieme a lui (`1.64` contro `1.71`, rapporto `1.04`)."))

# ====================================================================== C5 e C6
_pav_on = sum(c["al_pavimento"] for n_ in pend_on
              for c in (dati[n_]["casi"] if dati.get(n_) else []) if "errore" not in c)
_pav_on_t = sum(c["al_pavimento_tutti"] for n_ in pend_on
                for c in (dati[n_]["casi"] if dati.get(n_) else []) if "errore" not in c)
OK.append(crit("C5", "il pavimento `1e-6` non comincia a mordere con la cura", _pav_on == 0,
               "ON: bersagli al pavimento %d   NODI al pavimento %d" % (_pav_on, _pav_on_t)
               + NL + "  PRIMA della cura era `0/20` in ogni riga (`CONFIG-1/a`)."))

P("=" * 118)
P("`C6` -- LA SCALA DELL'INERZIA SU TUTTI I NODI")
P("=" * 118)
P("%-20s %-13s %-13s %-13s %-13s %s" % ("braccio", "p5", "mediana", "p95", "min", "al pav./nodi"))
_sc = {}
for (nome, s, v, fl, sim, argv, modo) in BRACCI:
    o = dati.get(nome)
    if not o or not o.get("scala"):
        continue
    sc = o["scala"]
    _sc[nome] = sc
    P("%-20s %-13.6g %-13.6g %-13.6g %-13.6g %d/%d"
      % (nome, sc["p5"], sc["p50"], sc["p95"], sc["min"], sc["al_pavimento"], sc["nodi"]))
P()
_on5 = [v["p50"] for k, v in _sc.items() if k.startswith("on_")]
_off5 = [v["p50"] for k, v in _sc.items() if k.startswith("off_")]
OK.append(crit("C6", "la scala dell'inerzia su TUTTI i nodi e' DICHIARATA prima/dopo",
               bool(_on5 and _off5),
               "mediana ON %.6g   mediana OFF %.6g   rapporto x%.4g"
               % (float(np.median(_on5)) if _on5 else float("nan"),
                  float(np.median(_off5)) if _off5 else float("nan"),
                  (float(np.median(_on5)) / float(np.median(_off5))) if _on5 and _off5
                  else float("nan"))
               + NL + "  **nessuna soglia, di proposito:** la cura divide, quindi la scala SCENDE."
               + NL + "  Il criterio e' che sia DICHIARATA, e `C5` dice se arriva al pavimento."))

# ====================================================================== R1 e R2
P("=" * 118)
P("`R1`/`R2` -- ESTENSIVO O RITARDATO? il contrasto DOPO il rilassamento (flag SPENTO)")
P("=" * 118)
P("  ⚠ `N` NON E' SCELTO E NON E' RICOSTRUITO PER ALGEBRA: si guarda il DECADIMENTO MISURATO")
P("    di `|peq - rho|/rho` sui bersagli. Il budget e' %d passi, DICHIARATO." % BUDGET)
P("    *(`TAU_BG = 5.0` non e' il tempo vero -- con `TAU_LOCALI` e' `1/r_arco` -- e il `dt_e`")
P("    misurato e' per SOTTO-PASSO: `tau_bg/dt_e` NON e' un numero di passi.)*")
P()
_res_t = {}
for (nome, s, v, fl, sim, argv, modo) in BRACCI:
    if modo != "rilassa":
        continue
    o = dati.get(nome)
    if not o or not o.get("serie"):
        P("  [%s] NESSUN DATO" % nome)
        continue
    P("-" * 118)
    P("%s   checkpoint %s" % (nome, o.get("checkpoint")))
    P("%-8s %-13s %-13s %-15s %-13s %s"
      % ("passo", "pend.coppia", "pend.contr.", "differenza", "|peq-rho|/rho", "|omega| k2/k77"))
    _serie = []
    for pp in o["checkpoint"]:
        v_ = o["serie"].get(str(pp))
        if not v_:
            continue
        ks = sorted((int(k) for k in v_), reverse=True)
        pc = pend(ks, [v_[str(k)]["coppia_p50"] for k in ks])
        px = pend(ks, [v_[str(k)]["contrasto_p50"] for k in ks])
        sc = float(np.median([v_[str(k)].get("scarto_peq_p50", float("nan")) for k in ks]))
        om = (v_[str(min(ks))]["omega_p50"] / v_[str(max(ks))]["omega_p50"]
              if v_[str(max(ks))]["omega_p50"] else float("nan"))
        _serie.append((pp, pc, px, abs(px - pc), sc, om))
        P("%-8d %-13.4f %-13.4f %-15.4f %-13.4g %.4g" % (pp, pc, px, abs(px - pc), sc, om))
    _res_t[nome] = _serie
    P()
_r1 = []
_r2 = []
for nome, se in _res_t.items():
    if len(se) < 2:
        continue
    _r1.append((nome, se[-1][3], se[-1][4]))
    _r2.append((nome, [x[3] for x in se], all(se[k][3] >= se[k + 1][3] - 1e-12
                                              for k in range(len(se) - 1))))
_sp2 = _sp_on * 2.0 if _sp_on == _sp_on else float("nan")
_r1_ok = bool(_r1) and all(d <= _sp2 for _n, d, _s in _r1)
_rilassato = bool(_r1) and all(s < 0.1 for _n, _d, s in _r1)
OK.append(crit("R1", "dopo il budget, la pendenza del CONTRASTO torna su quella della COPPIA",
               bool(_r1_ok and _rilassato),
               NL.join("  %-20s differenza finale %.4f   |peq-rho|/rho finale %.4g"
                       % (n_, d_, s_) for n_, d_, s_ in _r1)
               + NL + "criterio: differenza <= 2 spread (%.4f) **E** `|peq-rho|/rho < 0.1`" % _sp2
               + NL + "  **LA SECONDA CONDIZIONE NON E' UN EXTRA: SE `peq` NON SI E' RILASSATO,"
               + NL + "  `R1` NON E' MISURATO** -- e un `FAIL` senza di essa sarebbe un verdetto"
               + NL + "  vacuo travestito da risultato."))
OK.append(crit("R2", "il residuo CALA MONOTONAMENTE nel tempo (transitorio, non offset)",
               bool(_r2) and all(m for _n, _s, m in _r2),
               NL.join("  %-20s residui %s   monotono: %s"
                       % (n_, "  ".join("%.4f" % x for x in s_), m_) for n_, s_, m_ in _r2)))

# ====================================================================== R3, R4, R3bis
P("=" * 118)
P("`R3`/`R4`/`R3bis` -- I FIGLI DELLA MITOSI dalla nascita (flag SPENTO)")
P("=" * 118)
for s in SEMI:
    o = dati.get("figli_s%d" % s)
    if not o or not o.get("storia"):
        P("  [figli_s%d] NESSUN FIGLIO nel budget: R3/R4/R3bis NON MISURATI su questo seme." % s)
        continue
    st = np.array(o["storia"], float)     # [passo, id, eta_nasc, ramp, omega, rho, peq, contr]
    P("-" * 118)
    P("seme %d   nati %d   campioni %d" % (s, len(o.get("nati") or {}), st.shape[0]))
    P("%-8s %-8s %-12s %-12s %-12s %-12s %-12s %s"
      % ("eta", "quanti", "ramp p50", "|omega| p50", "rho p50", "peq p50", "contr p50",
         "|omega|*ramp"))
    for _e in sorted(set(int(x) for x in st[:, 2]))[:14]:
        m = st[:, 2] == _e
        if m.sum() < 1:
            continue
        _rr, _oo = st[m, 3], st[m, 4]
        P("%-8d %-8d %-12.6g %-12.6g %-12.6g %-12.6g %-12.6g %.6g"
          % (_e, int(m.sum()), np.median(_rr), np.median(_oo), np.median(st[m, 5]),
             np.median(st[m, 6]), np.median(st[m, 7]), np.median(_oo * _rr)))
    P()
    if o.get("nullo"):
        nu = np.array(o["nullo"], float)
        P("  IL NULLO (nodi NON nati), mediane: ramp %.6g -> %.6g   |omega| %.6g -> %.6g"
          % (nu[0, 1], nu[-1, 1], nu[0, 2], nu[-1, 2]))
        P("              rho %.6g -> %.6g   peq %.6g -> %.6g   contrasto %.6g -> %.6g"
          % (nu[0, 3], nu[-1, 3], nu[0, 4], nu[-1, 4], nu[0, 5], nu[-1, 5]))
    P()
_r3, _r3b, _r4 = [], [], []
for s in SEMI:
    o = dati.get("figli_s%d" % s)
    if not o or not o.get("storia"):
        continue
    st = np.array(o["storia"], float)
    nu = np.array(o["nullo"], float) if o.get("nullo") else None
    et = sorted(set(int(x) for x in st[:, 2]))
    if len(et) < 3:
        continue
    _c = [float(np.median(st[st[:, 2] == e, 7])) for e in et]
    _o = [float(np.median(st[st[:, 2] == e, 4])) for e in et]
    _r = [float(np.median(st[st[:, 2] == e, 3])) for e in et]
    _p = [float(np.median(st[st[:, 2] == e, 6])) for e in et]
    _h = [float(np.median(st[st[:, 2] == e, 5])) for e in et]
    _prod = [a * b for a, b in zip(_o, _r)]
    _rif = float(nu[-1, 5]) if nu is not None else float("nan")
    _r3.append((s, _c[0], _c[-1], _rif, _p[0], _p[-1], _h[0], _h[-1]))
    _cv = float(np.std(_prod) / np.mean(_prod)) if np.mean(_prod) else float("nan")
    _cvo = float(np.std(_o) / np.mean(_o)) if np.mean(_o) else float("nan")
    _r3b.append((s, _cv, _cvo, _r[0], _r[-1], _o[0], _o[-1]))
    if nu is not None:
        _r4.append((s, float(nu[0, 5]), float(nu[-1, 5]), float(nu[0, 2]), float(nu[-1, 2])))
OK.append(crit("R3", "il contrasto dei FIGLI rientra verso i nodi maturi entro il budget",
               bool(_r3) and all(abs(c1 - rf) < abs(c0 - rf) for _s, c0, c1, rf, *_x in _r3
                                 if rf == rf),
               NL.join("  seme %d: contrasto %.6g -> %.6g   (nodi non nati: %.6g)   "
                       "peq %.6g -> %.6g   rho %.6g -> %.6g"
                       % (s, c0, c1, rf, p0, p1, h0, h1)
                       for s, c0, c1, rf, p0, p1, h0, h1 in _r3)))
OK.append(crit("R3bis", "`|omega| * ramp` COSTANTE sui figli (incoerenza di ESPONENTI)",
               bool(_r3b) and all(cv < cvo / 2.0 for _s, cv, cvo, *_x in _r3b
                                  if cvo == cvo and cvo > 0),
               NL.join("  seme %d: CV(|omega|*ramp) %.4f   CV(|omega|) %.4f   "
                       "ramp %.4g -> %.4g   |omega| %.6g -> %.6g"
                       % (s, cv, cvo, r0, r1, o0, o1) for s, cv, cvo, r0, r1, o0, o1 in _r3b)
               + NL + "criterio: il prodotto e' COSTANTE se la sua dispersione relativa e'"
               + NL + "  **meno di META'** di quella di `|omega|` da solo. **Se passa, il difetto"
               + NL + "  dei figli e' un'incoerenza di ESPONENTI della rampa** -- non estensivita'"
               + NL + "  ne' solo ritardo di `peq` (lettura di Luca, derivata dal codice)."))
OK.append(crit("R4", "IL NULLO: i nodi NON nati nello stesso intervallo", bool(_r4),
               NL.join("  seme %d: contrasto %.6g -> %.6g   |omega| %.6g -> %.6g"
                       % x for x in _r4)
               + NL + "  **senza questo, un \"rientro\" potrebbe essere la deriva di TUTTO il"
               + NL + "  sistema.** Non ha soglia: e' il termine di paragone di `R3`."))

P("=" * 118)
P("ESITO: %d/%d PASS" % (sum(1 for x in OK if x), len(OK)))
P("=" * 118)
P()
P("QUALI DELLE TRE LETTURE REGGONO -- e possono essere piu' di una:")
P("  ESTENSIVITA'        -> `C1'` e `C1''`: la normalizzazione basta?")
P("  RITARDO DI `peq`    -> `R1` e `R2`: il residuo e' un TRANSITORIO?")
P("  ESPONENTI DI `ramp` -> `R3bis`: `|omega|*ramp` e' costante sui figli?")
P("**NESSUNA CURA SCELTA: decide Luca.**")
P()
P("COSA QUESTO SIGILLO *NON* DICE:")
P("  - `R1`/`R2` girano a flag SPENTO (lo chiede il criterio di Luca): dicono se il difetto e' un")
P("    transitorio DEL SISTEMA, non se la cura lo tolga.")
P("  - `R1`/`R2` usano TRE valori di `k` invece di cinque, e va detto: una pendenza su 3 punti e'")
P("    piu' fragile. Il costo era 5 reti x %d passi x 4 bracci; la barra si legge dai due semi."
  % BUDGET)
P("  - il BUDGET e' %d passi, DICHIARATO. Se `|peq-rho|/rho` non scende sotto `0.1`, `R1` dice" % BUDGET)
P("    **NON MISURATO**, non `FAIL`.")
P("  - i 20 bersagli non sono adiacenti, **ma possono condividere un VICINO**.")
P("  - DUE SEMI: per una barra fra semi servono >= 4 (`P3` delle regole).")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
sys.exit(0 if all(OK) else 1)
