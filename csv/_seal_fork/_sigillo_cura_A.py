r"""SIGILLO **CURA A** — `rho_s / W^2` NEL SOLO CONTRASTO *(decisione di Luca, 2026-09-26)*.

I criteri stanno in `doc/TASK_HISTORY/2026-09-26_cura-A-rho-su-W2.md`, **committato PRIMA del
codice**.

```
C1'        sul TAGLIO: pendenza del contrasto = quella della coppia entro 2x lo spread fra semi
F1         FIGLI: contrasto_figlio/contrasto_maturo allo STESSO PASSO, eta' 2..14
           atteso exp(T1+T3) ~ 2.5, accettabile fra 1.5 e 4        <- CALCOLATO DAI DATI
F2         |omega| figlio / |omega| maturo allo stesso passo, dall'eta' 2:  < 10
           **se FALLISCE, si identifica QUALE ADDENDO di omega_new domina e si FERMA**
C3         localita': byte-identita' a flag SPENTO contro il codice PRECEDENTE (`P8`)
C5         il pavimento 1e-6: quante volte morde     <- IL RISCHIO VERO di questa cura
P1-sexies  IL BRACCIO CON `/W` DEVE FALLIRE `C1'`
```

**IL BRACCIO `/W` viene dal PADRE del commit che ha introdotto `_wn * _wn`** — trovato con
`_cli_flag.sim_prima_del_flag("_wn * _wn", …)`, che **asserisce** che il file estratto non contenga
quella forma. **Non `HEAD`** (`P8`): `HEAD` contiene la cura.

**Tutto dal CLI** (`P3`), **`P5`** *(configurazione intera nel referto)*, **`P9`** *(la copia
diagnostica si genera al run e la postcondizione pretende che differisca solo per le righe
dichiarate)*, **un processo per braccio** (`STANDARD 1`), **riprendibile** *(json col blob)*.

**NESSUNA SECONDA CURA. Se `F2` cade, si nomina il termine e si FERMA.**

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
FUORI = os.path.join(_QUI, "_sig_cura_A")
DEST = os.path.join(FUORI, "SIGILLO_cura_A.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)
NL = chr(10)

# [`C1''''`, decisione di Luca 2026-09-26] **QUATTRO SEMI**, perche' `P3` delle regole lo impone
#   per una barra FRA SEMI: con 2 semi la deviazione standard ha UN grado di liberta'.
#   ⚠ **SOLO IL TAGLIO si rifa'**: `F1`, `F2`, `C3` e `C5` sono chiusi a 2 semi e **non si
#   ripetono** (ordine di Luca). I bracci `figli` restano quelli, e il referto lo dichiara.
SEMI = [11, 12, 13, 14]
SEMI_FIGLI = [11, 12]      # i bracci dei figli NON si rifanno: 2 semi, come sigillati
SEP = 4.0
GRADI = [77, 20, 8, 4, 2]
VERSI = ["lunghi", "corti"]
PASSI_PRIMA = 20
BUDGET = 120
BERSAGLI = 20
ETA_MAX = 14
OPZ = "--contrasto-intensivo"
FLAGNOME = "CONTRASTO_INTENSIVO"

SIM = os.path.join(RADICE, "soliton_simulator.py")
blob_vero = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()[:8]

DIAG_IN = [
    "        self._diag_inerzia = np.array(inerzia, copy=True)",
    "        self._diag_contrasto = np.array(_contrasto, copy=True)",
    "        self._diag_peq_nodo = np.array(_peq_nodo, copy=True)",
    "        self._diag_rho_s = np.array(_rho_s, copy=True)",
    "        self._diag_ok_n = np.array(_ok_n, copy=True)",
    "        self._diag_W = ((np.bincount(self.i, np.asarray(w, float), minlength=n)[:n]"
    " + np.bincount(self.j, np.asarray(w, float), minlength=n)[:n])"
    " if (w is not None and len(np.asarray(w)) == len(self.i)) else np.zeros(n))",
    "        self._diag_T2f = np.array(_T2, copy=True)",
]
# gli ADDENDI di `omega_new`, per `F2`: si leggono DOVE sono, non si ricostruiscono
DIAG_CO = [
    "        self._diag_coppia = np.array(correzione, copy=True)",
    "        self._diag_om_src = np.array(omega_src, copy=True)",
    # ❌ **DIFETTO MIO, e la regola che ho violato e' quella che Luca aveva imposto:** avevo
    #   scritto `omega_src / _tau[:, None]`, **riscrivendo** l'espressione invece di **copiarla**.
    #   `_tau` e' **GIA'** `[:, None]` (`:3584`, `:3589`) oppure uno **scalare** (`:3591`), quindi
    #   il mio `[:, None]` lo rendeva `(n,1,1)` e il broadcast produceva `(n,n,3)`: i tre bracci
    #   dei figli sono morti con `TypeError: only length-1 arrays can be converted to Python
    #   scalars`. **E' la stessa famiglia del «ricostruire la coppia da fuori», che dava META'
    #   COPPIA:** l'unica forma sicura e' **la stessa riga del codice**, copiata.
    "        self._diag_freno = np.array(omega_src / _tau, copy=True)",
]


def copia_diag(sorgente, dest):
    """La copia si GENERA al run, e la POSTCONDIZIONE pretende che differisca solo per le righe
    dichiarate (`P9`). Restituisce `(blob, ancore)`."""
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
    import difflib as _dl
    _dop = io.open(dest, encoding="utf-8", newline="").read().split(NL)
    _agg = [x[2:].rstrip(chr(13)) for x in _dl.ndiff(righe, _dop) if x.startswith("+ ")]
    _tol = [x[2:].rstrip(chr(13)) for x in _dl.ndiff(righe, _dop) if x.startswith("- ")]
    _est = [x for x in _agg if x not in set(DIAG_IN) | set(DIAG_CO)]
    assert not _est and not _tol, ("la copia differisce per righe NON dichiarate: aggiunte %r  "
                                  "tolte %r" % (_est[:2], _tol[:2]))
    ast.parse(NL.join(_dop))
    return hashlib.sha1(io.open(dest, "rb").read()).hexdigest()[:8], k


COPIA = os.path.join(FUORI, "_sim_A.py")
blob_copia, anc = copia_diag(SIM, COPIA)

# ---------------------------------------------------- il braccio `/W`: il PADRE del commit di `W^2`
PRIMA_W = os.path.join(TMP, "_sim_su_W.py")
COMMIT_A = _cli_flag.sim_prima_del_flag("_wn * _wn", PRIMA_W, radice=RADICE)
PRIMA_W_DIAG = os.path.join(TMP, "_sim_su_W_diag.py")
blob_W, anc_W = copia_diag(PRIMA_W, PRIMA_W_DIAG)

# ---------------------------------------------------- il codice PRECEDENTE al flag, per `C3`
PRIMA_FLAG = os.path.join(TMP, "_sim_prima_flag.py")
COMMIT_FLAG = _cli_flag.sim_prima_del_flag(FLAGNOME, PRIMA_FLAG, radice=RADICE)
PRIMA_FLAG_DIAG = os.path.join(TMP, "_sim_prima_flag_diag.py")
blob_pf, anc_pf = copia_diag(PRIMA_FLAG, PRIMA_FLAG_DIAG)

_S0, ARGV = _cli_flag.argv_del_driver([], dest=os.path.join(TMP, "_scarto"))
ARGV = ARGV + ["--nodi", "0"]
ARGV_ON = ARGV + [OPZ]
ARGV_OFF = list(ARGV)

FIGLIO = r'''
import copy as _copy
import datetime as _dt
import hashlib as _h
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import _cli_flag
import _passo
_argv, _scart = _cli_flag.argv_per(SIM, ARGV)
S, _a = _cli_flag.carica_dal_cli(_argv, nome="sim_A", sim=SIM)
o = dict(NOME=NOME, SEME=SEME, VERSO=VERSO, MODO=MODO, blob_sim=BLOB_SIM, blob_copia=BLOB_COPIA,
         quando=_dt.datetime.now().isoformat(), completo=False,
         CFG={"flag": getattr(S, FLAGNOME, "ASSENTE"), "atteso": bool(FLAG),
              "opz": OPZ in _argv, "scartate": _scart, "sim": os.path.basename(SIM)})
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
for _ in range(PASSI_PRIMA):
    _passo.passo_pieno(S, net)


def _dg(nt, nome):
    return np.asarray(getattr(nt, nome, []), float)


def _ramp(nt):
    _tr = nt._tempo_rampa()
    return np.minimum(1.0, np.asarray(nt.eta, float) / _tr)


# =============================================================== MODO `taglio`: `C1'`, `C3`, `C5`
if MODO == "taglio":
    n = int(net.n)
    ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
    mm = (ii < n) & (jj < n)
    gr = np.zeros(n, int)
    np.add.at(gr, ii[mm], 1); np.add.at(gr, jj[mm], 1)
    gm = int(np.median(gr))
    _ok = np.where(gr >= max(GRADI))[0]
    _ok = _ok[np.argsort(np.abs(gr[_ok] - gm))]
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
        BERS.append(_c); presi.add(_c); presi |= vic.get(_c, set())
        if len(BERS) >= BERSAGLI:
            break
    o["bersagli"] = [int(b) for b in BERS]
    _in0 = _dg(net, "_diag_inerzia")
    if _in0.size:
        o["scala"] = dict(p5=float(np.percentile(_in0, 5)), p50=float(np.median(_in0)),
                          p95=float(np.percentile(_in0, 95)), min=float(_in0.min()),
                          al_pavimento=int(np.sum(_in0 <= 1e-6)), nodi=int(_in0.size))
    o["firme"] = {}
    for k, v in sorted(vars(net).items()):
        if k.startswith("_g_") or k.startswith("_diag"):
            continue
        if isinstance(v, np.ndarray):
            o["firme"][k] = [_h.sha1(np.ascontiguousarray(v).tobytes()).hexdigest()[:12],
                             list(v.shape), str(v.dtype)]
        elif isinstance(v, (int, float, bool, str)):
            o["firme"][k] = [_h.sha1(repr(v).encode()).hexdigest()[:12], [], type(v).__name__]
    d = np.asarray(net.d, float)
    suoi = {b: np.where((ii == b) | (jj == b))[0] for b in BERS}
    o["casi"] = []
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
            _in, _ct = _dg(net2, "_diag_inerzia"), _dg(net2, "_diag_contrasto")
            _co = _dg(net2, "_diag_coppia")
            _okn = np.asarray(getattr(net2, "_diag_ok_n", []), bool)
            _om = np.linalg.norm(np.asarray(net2.omega_s, float), axis=1)
            B = np.array([b for b in BERS if b < _in.size and b < _om.size
                          and (b >= _okn.size or _okn[b])], int)
            cop = np.linalg.norm(_co[B], axis=1) if _co.size and B.size else np.zeros(0)
            o["casi"].append(dict(K=int(K), quanti=int(B.size),
                                 coppia_p50=float(np.median(cop)) if cop.size else float("nan"),
                                 inerzia_p50=float(np.median(_in[B])) if B.size else float("nan"),
                                 contrasto_p50=float(np.median(_ct[B])) if B.size else float("nan"),
                                 omega_p50=float(np.median(_om[B])) if B.size else float("nan"),
                                 al_pavimento=int(np.sum(_in[B] <= 1e-6)) if B.size else -1,
                                 al_pav_tutti=int(np.sum(_in <= 1e-6)) if _in.size else -1,
                                 nodi=int(_in.size)))
        except Exception as e:
            o["casi"].append(dict(K=int(K), errore=str(e)[:200]))

# =============================================================== MODO `figli`: `F1`, `F2`
elif MODO == "figli":
    n0 = int(net.n)
    o["n0"] = n0
    o["righe"] = []
    o["passi_con_nascite"] = 0
    o["ok_n_falsi_figli"] = 0
    nati = {}
    for _p in range(1, BUDGET + 1):
        _pre = int(net.n)
        _passo.passo_pieno(S, net)
        if int(net.n) > _pre:
            for _k in range(_pre, int(net.n)):
                nati[_k] = _p
        W = _dg(net, "_diag_W"); CT = _dg(net, "_diag_contrasto"); IN = _dg(net, "_diag_inerzia")
        PQ = _dg(net, "_diag_peq_nodo"); RH = _dg(net, "_diag_rho_s")
        CO = _dg(net, "_diag_coppia"); OS = _dg(net, "_diag_om_src"); FR = _dg(net, "_diag_freno")
        assert hasattr(net, "_diag_ok_n"), "manca `_diag_ok_n`"
        OKN = np.asarray(net._diag_ok_n, bool)
        _nd = int(min(W.size, CT.size, IN.size, PQ.size, RH.size, OKN.size,
                      CO.shape[0], OS.shape[0], FR.shape[0]))
        if _nd < 10:
            continue
        if _nd < int(net.n):
            o["passi_con_nascite"] += 1
        n = _nd
        cop = np.linalg.norm(CO[:n], axis=1)
        osr = np.linalg.norm(OS[:n], axis=1)
        fre = np.linalg.norm(FR[:n], axis=1)
        om = np.linalg.norm(np.asarray(net.omega_s, float), axis=1)[:n]
        rmp = _ramp(net)[:n]
        mv = np.arange(min(n0, n))
        bm = (W[mv] > 0) & (PQ[mv] > 0) & (RH[mv] > 0) & (CT[mv] > 0) & OKN[mv]
        _mv = mv[bm]
        if _mv.size < 10:
            continue
        # i MATURI: media GEOMETRICA (additiva nei logaritmi), allo STESSO PASSO
        _cm = float(np.exp(np.mean(np.log(CT[_mv]))))
        _om_m = float(np.exp(np.mean(np.log(np.maximum(om[_mv], 1e-300)))))
        _in_m = float(np.exp(np.mean(np.log(IN[_mv]))))
        _co_m = float(np.exp(np.mean(np.log(np.maximum(cop[_mv], 1e-300)))))
        _os_m = float(np.exp(np.mean(np.log(np.maximum(osr[_mv], 1e-300)))))
        _fr_m = float(np.exp(np.mean(np.log(np.maximum(fre[_mv], 1e-300)))))
        for _k, _nasc in nati.items():
            _e = _p - _nasc
            if _k >= n or _e < 1 or _e > ETA_MAX:
                continue
            if not OKN[_k]:
                o["ok_n_falsi_figli"] += 1
                continue
            o["righe"].append([_p, int(_k), int(_e), float(CT[_k]), _cm, float(om[_k]), _om_m,
                               float(IN[_k]), _in_m, float(cop[_k]), _co_m,
                               float(osr[_k]), _os_m, float(fre[_k]), _fr_m, float(rmp[_k]),
                               float(W[_k])])
    o["nati"] = len(nati)

o["completo"] = True
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  modo %s  n %d" % (NOME, MODO, net.n))
'''


def riusabile(nome, blobc):
    p = os.path.join(TMP, nome + ".json")
    if not os.path.exists(p):
        return False, "assente"
    try:
        o = json.loads(io.open(p, encoding="utf-8").read())
    except Exception as e:
        return False, "illeggibile (%s)" % str(e)[:40]
    if not o.get("completo"):
        return False, "INCOMPLETO"
    if o.get("blob_sim") != blob_vero or o.get("blob_copia") != blobc:
        return False, "BLOB DIVERSO (%s/%s)" % (o.get("blob_sim"), o.get("blob_copia"))
    return True, o


def braccio(nome, seme, verso, flag, sim, blobc, argv, modo):
    testa = ["RAD = %r" % RADICE, "TMPD = %r" % TMP, "NOME = %r" % nome, "SEME = %d" % seme,
             "SEP = %r" % SEP, "SIM = %r" % sim, "GRADI = %r" % GRADI,
             "PASSI_PRIMA = %d" % PASSI_PRIMA, "BUDGET = %d" % BUDGET,
             "BERSAGLI = %d" % BERSAGLI, "ETA_MAX = %d" % ETA_MAX, "VERSO = %r" % verso,
             "ARGV = %r" % argv, "FLAG = %r" % flag, "OPZ = %r" % OPZ,
             "FLAGNOME = %r" % FLAGNOME, "MODO = %r" % modo,
             "BLOB_SIM = %r" % blob_vero, "BLOB_COPIA = %r" % blobc, ""]
    p = os.path.join(TMP, "_br_%s.py" % nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(NL.join(testa) + FIGLIO)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


BRACCI = []
for s in SEMI:
    for v in VERSI:
        BRACCI.append(("on_s%d_%s" % (s, v), s, v, True, COPIA, blob_copia, ARGV_ON, "taglio"))
        BRACCI.append(("off_s%d_%s" % (s, v), s, v, False, COPIA, blob_copia, ARGV_OFF, "taglio"))
        # `P1-sexies`: IL BRACCIO CON `/W`, che DEVE fallire `C1'`
        BRACCI.append(("suW_s%d_%s" % (s, v), s, v, True, PRIMA_W_DIAG, blob_W, ARGV_ON, "taglio"))
for s in SEMI_FIGLI:
    BRACCI.append(("pf_s%d_lunghi" % s, s, "lunghi", False, PRIMA_FLAG_DIAG, blob_pf, ARGV_OFF,
                   "taglio"))
    BRACCI.append(("figli_on_s%d" % s, s, "lunghi", True, COPIA, blob_copia, ARGV_ON, "figli"))
    BRACCI.append(("figli_off_s%d" % s, s, "lunghi", False, COPIA, blob_copia, ARGV_OFF,
                   "figli"))

LOG, RIPRESI, dati = [], {}, {}
GRUPPI = [("taglio", [b for b in BRACCI if b[7] == "taglio"]),
          ("figli", [b for b in BRACCI if b[7] == "figli"])]
for _gn, _gb in GRUPPI:
    proc = {}
    for (nome, s, v, fl, sim, blobc, argv, modo) in _gb:
        ok, res = riusabile(nome, blobc)
        if ok:
            dati[nome] = res
            RIPRESI[nome] = (res.get("quando"), res.get("blob_sim"), res.get("blob_copia"))
            LOG.append("[%s] RIPRESO dal %s" % (nome, res.get("quando")))
            continue
        LOG.append("[%s] si gira: %s" % (nome, res))
        proc[nome] = braccio(nome, s, v, fl, sim, blobc, argv, modo)
    for nome, pr in proc.items():
        so, se = pr.communicate()
        LOG.append("[%s] rc=%d %s" % (nome, pr.returncode,
                                      (so or b"").decode("utf-8", "replace").strip()[-90:]))
        if pr.returncode:
            LOG.append((se or b"").decode("utf-8", "replace")[-1300:])
        else:
            _o, _r = riusabile(nome, [b[5] for b in _gb if b[0] == nome][0])
            if _o:
                dati[nome] = _r
    io.open(os.path.join(FUORI, "_PARZIALE_%s.txt" % _gn), "w", encoding="utf-8",
            newline=NL).write(NL.join(LOG) + NL)

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


def pend(x, y):
    x = np.log(np.asarray(x, float))
    y = np.asarray(y, float)
    m = np.isfinite(y) & (y > 0) & np.isfinite(x)
    if m.sum() < 3:
        return float("nan")
    return float(np.polyfit(x[m], np.log(y[m]), 1)[0])


P("=" * 116)
P("SIGILLO **CURA A** -- `rho_s / W^2` NEL SOLO CONTRASTO   (2026-09-26)")
P("=" * 116)
P()
for l in LOG:
    P(l)
P()
P("blob del simulatore      %s     copia diagnostica %s  (%d ancore, GENERATA AL RUN)"
  % (blob_vero, blob_copia, anc))
P("il braccio `/W` viene da %s^   (PADRE del commit di `_wn * _wn`, NON `HEAD`)  copia %s"
  % (COMMIT_A[:8], blob_W))
P("il codice PRIMA del flag %s^   (per `C3`)                                      copia %s"
  % (COMMIT_FLAG[:8], blob_pf))
P("semi %s   versi %s   k %s   bersagli %d   budget figli %d"
  % (SEMI, VERSI, GRADI, BERSAGLI, BUDGET))
if RIPRESI:
    P()
    P("BRACCI RIPRESI: %s" % ", ".join(sorted(RIPRESI)))
P()
_Sq, _ = _cli_flag.carica_dal_cli(_cli_flag.argv_per(COPIA, ARGV_ON)[0], nome="cfgA", sim=COPIA)
_cli_flag.dichiara_configurazione(
    _Sq, P, esenzione="il flag in prova NON e' ancora nel driver (entra dopo il sigillo): l'argv ON "
                      "e' quella del driver PIU' %s" % OPZ)

if any("rc=1" in l for l in LOG):
    P("STOP: un braccio non e' arrivato in fondo. Nessun criterio si legge.")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL.join(R))
    sys.exit(1)

OK = []

# ====================================================================== `C1'` e il braccio `/W`
P("=" * 116)
P("`C1'` -- LE PENDENZE SU `log k`: CONTRASTO contro COPPIA")
P("=" * 116)
P("%-18s %-14s %-14s %-14s %s" % ("braccio", "pend.coppia", "pend.contrasto", "differenza",
                                  "|omega| k2/k77"))
dif = {"on": [], "off": [], "suW": [], "pf": []}
for (nome, s, v, fl, sim, blobc, argv, modo) in BRACCI:
    if modo != "taglio":
        continue
    o = dati.get(nome)
    if not o:
        continue
    cc = [c for c in o["casi"] if "errore" not in c]
    if len(cc) < 3:
        continue
    ks = [c["K"] for c in cc]
    pc = pend(ks, [c["coppia_p50"] for c in cc])
    px = pend(ks, [c["contrasto_p50"] for c in cc])
    ro = (cc[-1]["omega_p50"] / cc[0]["omega_p50"]) if cc[0]["omega_p50"] else float("nan")
    fam = nome.split("_")[0]
    dif.setdefault(fam, []).append((nome, abs(px - pc), ro))
    P("%-18s %-14.4f %-14.4f %-14.4f x%.4g" % (nome, pc, px, abs(px - pc), ro))
P()
_don = [d for _n, d, _r in dif["on"]]
_sp = float(np.std(_don)) if len(_don) > 1 else float("nan")
# ============================================================== `C1''''`: la forma di Luca
#   ❌ **IL CRITERIO VECCHIO ERA AUTO-REFERENZIALE:** `max(|Δ| ON) <= 2*std(|Δ| ON)`. La soglia
#     si stringeva **con** i valori che doveva giudicare, e nel limite di una cura perfetta
#     **tendeva a zero**. Su 2 semi dava `FAIL` per **un solo** valore (`0.1167` contro `0.0752`),
#     mentre il divario era sceso di un fattore **20-100**.
#   ❌ **E LA MIA PROPOSTA «un decimo di OFF» E' STATA RIFIUTATA DA LUCA, con ragione:** avrebbe
#     dato `0.12` contro `0.125`, cioe' **un margine del 4 % su una soglia scelta GUARDANDO IL
#     RISULTATO**. `P1-sexies` nel modo piu' elegante.
#   ✅ **LA FORMA DI LUCA, su 4 SEMI:** la **MEDIA** e' compatibile con **ZERO** entro **2 ERRORI
#     STANDARD** *(`SE = std/sqrt(4)`, l'errore DELLA MEDIA, non la dispersione dei valori)*,
#     **e** sta **sotto** quella del braccio `/W` — che e' **un'altra popolazione MISURATA**,
#     non se stessa.
_m_on = float(np.mean(_don)) if _don else float("nan")
_se_on = (float(np.std(_don, ddof=1)) / np.sqrt(len(_don))) if len(_don) > 1 else float("nan")
_m_suw = float(np.mean([d for _n, d, _r in dif["suW"]])) if dif["suW"] else float("nan")
_a_ok = bool(_m_on == _m_on and _se_on == _se_on and _m_on <= 2.0 * _se_on)
_b_ok = bool(_m_on == _m_on and _m_suw == _m_suw and _m_on < _m_suw)
OK.append(crit("C1''''", "media di |pend(contrasto)-pend(coppia)| ON compatibile con ZERO (2 SE) E sotto `/W`",
               _a_ok and _b_ok,
               "ON  (`/W^2`), %d semi: %s" % (len(_don), "  ".join("%.4f" % d for d in _don))
               + NL + "   media %.4f   SE %.4f   ->  2 SE = %.4f   %s"
               % (_m_on, _se_on, 2.0 * _se_on,
                  "COMPATIBILE CON ZERO" if _a_ok else "NON compatibile")
               + NL + "`/W`   media %.4f   %s" % (_m_suw,
                                                  "ON sta SOTTO" if _b_ok else "ON NON sta sotto")
               + NL + "OFF  : %s" % "  ".join("%.4f" % d for _n, d, _r in dif["off"])
               + NL + "`/W`  : %s" % "  ".join("%.4f" % d for _n, d, _r in dif["suW"])
               + NL + "  **Nessun numero scelto:** il `2` degli errori standard e' la convenzione"
               + NL + "  statistica. E con 4 semi `t(0.025,3) = 3.18`, quindi **`2 SE` e' PIU'"
               + NL + "  SEVERO** di un IC95 vero: lo dichiaro invece di spacciarlo per uguale."))
_dsuw = [d for _n, d, _r in dif["suW"]]
OK.append(crit("P1-sexies", "IL BRACCIO CON `/W` FALLISCE `C1'` (il caso che deve fallire)",
               bool(_dsuw and _don and min(_dsuw) > max(_don)),
               "`/W`  : %s" % "  ".join("%.4f" % d for d in _dsuw)
               + NL + "`/W^2`: %s" % "  ".join("%.4f" % d for d in _don)
               + NL + "criterio: **il minimo di `/W` sta SOPRA il massimo di `/W^2`**, cioe' le due"
               + NL + "  popolazioni non si toccano. Se si toccassero, `C1'` non distinguerebbe le"
               + NL + "  due forme, e il suo PASS sarebbe casuale."))

# ====================================================================== `C3`
_ok3, _det3 = True, []
for s in SEMI:
    a = dati.get("off_s%d_lunghi" % s)
    b = dati.get("pf_s%d_lunghi" % s)
    if not a or not b or "firme" not in a or "firme" not in b:
        _ok3 = False
        _det3.append("seme %d: dati mancanti" % s)
        continue
    com = sorted(set(a["firme"]) & set(b["firme"]))
    dd = [k for k in com if a["firme"][k] != b["firme"][k]]
    sa = sorted(set(a["firme"]) - set(b["firme"]))
    sb = sorted(set(b["firme"]) - set(a["firme"]))
    _ok3 = _ok3 and not dd and not sa and not sb
    _det3.append("seme %d: campi %d   DIVERSI %d   solo nuovo %s   solo vecchio %s"
                 % (s, len(com), len(dd), sa or "nessuno", sb or "nessuno"))
OK.append(crit("C3", "flag SPENTO byte-identico al codice PRECEDENTE (%s^)" % COMMIT_FLAG[:8],
               _ok3, NL.join(_det3)))

# ====================================================================== `C5`
P("=" * 116)
P("`C5` -- IL PAVIMENTO `1e-6`: **IL RISCHIO VERO DI QUESTA CURA**")
P("=" * 116)
P("%-18s %-13s %-13s %-13s %-13s %s" % ("braccio", "p5", "mediana", "p95", "min", "al pav./nodi"))
_pav_on = 0
for (nome, s, v, fl, sim, blobc, argv, modo) in BRACCI:
    o = dati.get(nome)
    if not o or not o.get("scala"):
        continue
    sc = o["scala"]
    if nome.startswith("on_"):
        _pav_on += sc["al_pavimento"]
    P("%-18s %-13.6g %-13.6g %-13.6g %-13.6g %d/%d"
      % (nome, sc["p5"], sc["p50"], sc["p95"], sc["min"], sc["al_pavimento"], sc["nodi"]))
_pav_casi = sum(c.get("al_pav_tutti", 0) for n_ in dati if n_.startswith("on_")
                for c in dati[n_].get("casi", []) if "errore" not in c)
P()
OK.append(crit("C5", "il pavimento `1e-6` non morde con `/W^2`", _pav_on == 0 and _pav_casi == 0,
               "al passo zero, nodi al pavimento (ON): %d" % _pav_on
               + NL + "nei casi tagliati, nodi al pavimento (ON, sommati): %d" % _pav_casi
               + NL + "  **dividere per `W^2` abbassa l'inerzia DUE volte**: con `/W` il minimo era"
               + NL + "  `0.0655`, quattro ordini sopra `1e-6`. **Qui si misura, non si spera.**"))

# ====================================================================== `F1` e `F2`
P("=" * 116)
P("`F1`/`F2` -- I FIGLI contro i MATURI **DELLO STESSO PASSO** (media geometrica)")
P("=" * 116)
P("%-16s %-6s %-8s %-13s %-13s %-13s %s"
  % ("braccio", "eta", "campioni", "c_f/c_m", "|om|_f/|om|_m", "in_f/in_m", "ramp p50"))
_f1, _f2, _dom = {}, {}, {}
for (nome, s, v, fl, sim, blobc, argv, modo) in BRACCI:
    if modo != "figli":
        continue
    o = dati.get(nome)
    if not o or not o.get("righe"):
        P("  [%s] NESSUN FIGLIO nel budget" % nome)
        continue
    ar = np.array(o["righe"], float)
    # [passo,id,eta, ct,cm, om,om_m, in,in_m, co,co_m, os,os_m, fr,fr_m, ramp, W]
    et = sorted(set(int(x) for x in ar[:, 2]))
    et = [e for e in et if e >= 2]
    r1, r2 = [], []
    for e in et:
        m = ar[:, 2] == e
        _rc = float(np.exp(np.mean(np.log(ar[m, 3] / ar[m, 4]))))
        _ro = float(np.exp(np.mean(np.log(np.maximum(ar[m, 5], 1e-300) / ar[m, 6]))))
        _ri = float(np.exp(np.mean(np.log(ar[m, 7] / ar[m, 8]))))
        r1.append(_rc); r2.append(_ro)
        if e in (2, 8, 14):
            P("%-16s %-6d %-8d %-13.6g %-13.6g %-13.6g %.4g"
              % (nome, e, int(m.sum()), _rc, _ro, _ri, float(np.median(ar[m, 15]))))
    _f1[nome] = r1
    _f2[nome] = r2
    # gli ADDENDI di `omega_new`, per il caso in cui `F2` cada
    _dom[nome] = {}
    for _i, _im, _nm in ((9, 10, "correzione"), (11, 12, "omega_src"), (13, 14, "freno")):
        _dom[nome][_nm] = float(np.exp(np.mean(np.log(
            np.maximum(ar[:, _i], 1e-300) / np.maximum(ar[:, _im], 1e-300)))))
    _dom[nome]["corr/inerzia"] = float(np.exp(np.mean(np.log(
        np.maximum(ar[:, 9], 1e-300) / ar[:, 7])))) / float(np.exp(np.mean(np.log(
            np.maximum(ar[:, 10], 1e-300) / ar[:, 8]))))
P()
_f1on = [x for n_, v_ in _f1.items() if n_.startswith("figli_on") for x in v_]
_f1off = [x for n_, v_ in _f1.items() if n_.startswith("figli_off") for x in v_]
OK.append(crit("F1", "`contrasto_figlio/contrasto_maturo` fra `1.5` e `4` (atteso `~2.5`)",
               bool(_f1on) and all(1.5 <= x <= 4.0 for x in _f1on),
               "ON  (`/W^2`): min %.4g   mediana %.4g   max %.4g   (n=%d)"
               % (min(_f1on), float(np.median(_f1on)), max(_f1on), len(_f1on)) if _f1on else "ON: -"
               + NL
               + (NL + "OFF         : min %.4g   mediana %.4g   max %.4g   <- IL NULLO"
                  % (min(_f1off), float(np.median(_f1off)), max(_f1off)) if _f1off else "")
               + NL + "  **La previsione `~2.5` e' CALCOLATA DAI DATI** (`exp(T1+T3)`: min `2.3265`,"
               + NL + "  mediana `2.4567`, max `2.5387` su 26 punti), non scelta."))
_f2on = [x for n_, v_ in _f2.items() if n_.startswith("figli_on") for x in v_]
_f2off = [x for n_, v_ in _f2.items() if n_.startswith("figli_off") for x in v_]
OK.append(crit("F2", "`|omega|_figlio/|omega|_maturo` < 10 dall'eta' 2",
               bool(_f2on) and max(_f2on) < 10.0,
               ("ON  (`/W^2`): min %.4g   mediana %.4g   max %.4g"
                % (min(_f2on), float(np.median(_f2on)), max(_f2on))) if _f2on else "ON: -"
               + (NL + "OFF         : min %.4g   mediana %.4g   max %.4g   <- IL NULLO"
                  % (min(_f2off), float(np.median(_f2off)), max(_f2off)) if _f2off else "")))

if _f2on and max(_f2on) >= 10.0:
    P("=" * 116)
    P("`F2` E' CADUTO: **QUALE ADDENDO DI `omega_new` DOMINA SUI FIGLI** (ordine di Luca)")
    P("=" * 116)
    P("  `omega_new = omega_src + dt_n * (correzione/inerzia - omega_src/_tau)`")
    P("  rapporti figlio/maturo, media geometrica su tutte le eta':")
    P()
    P("%-16s %-16s %-16s %-16s %s" % ("braccio", "correzione", "omega_src", "freno",
                                      "corr/inerzia"))
    for n_ in sorted(_dom):
        d_ = _dom[n_]
        P("%-16s %-16.6g %-16.6g %-16.6g %.6g"
          % (n_, d_["correzione"], d_["omega_src"], d_["freno"], d_["corr/inerzia"]))
    P()
    P("  **SI NOMINA IL TERMINE E SI FERMA: nessuna seconda cura** (ordine di Luca).")
    P()

P("=" * 116)
P("ESITO: %d/%d PASS" % (sum(1 for x in OK if x), len(OK)))
P("=" * 116)
P()
P("COSA QUESTO SIGILLO *NON* DICE:")
P("  - **`R3bis` e' caduto**: la coppia non porta `ramp` (`^0.15`, `^0.04`), quindi l'asimmetria")
P("    sui figli e' `0` contro `2.8` e `W^2` ne toglie `2`: **resta `0.8`**. Questa cura non")
P("    chiude quello, ed era scritto PRIMA.")
P("  - `C1'` (taglio) e `F1` (figli) guardano **due popolazioni diverse** e possono dare esiti")
P("    diversi. **Se succede si riporta, non si scegle quale contare.**")
P("  - DUE SEMI: per una barra fra semi servono >= 4 (`P3`).")
P("  - i 20 bersagli non sono adiacenti, ma possono **condividere un vicino**.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
sys.exit(0 if all(OK) else 1)
