# -*- coding: utf-8 -*-
"""**`A13` ALLA NASCITA, MISURATO IN MODO RELAZIONALE** *(correzione di Luca, 2026-09-25)*.

> *«`pos` è il disegno; la distanza fra due nodi è quella LUNGO GLI ARCHI. Il figlio dista `d/2`
> dai genitori e di più da tutti gli altri: `A13` alla nascita equivale a «l'arco che si divide
> ha `d >= 2 LAM`» (= `U2`). MISURA: la frazione di mitosi con `d_arco >= 2 LAM`, e per lo
> Schwinger la `d` dei nuovi archi (oggi presa da `pos`: voce `A3`).»*

**DOVE SI LEGGE LA `d` GREZZA, e non serve indovinarla:** `_nasce(v, dove, md, md0)` riceve
**`v` PRIMA del troncamento**. Nel sito `mitosi` con la chiamata `dh`, **`v` è esattamente
`d_arco/2`**; nel sito `schwinger`, `v` è `max(0.5·|pos[aa]−pos[bb]|, 0.05)`.

```
mitosi      d_arco = 2 * v          ->  A13 alla nascita  <=>  d_arco >= 2 LAM  <=>  v >= LAM
schwinger   v viene da `pos`        ->  e' la voce `A3`: la lunghezza di un arco nuovo
                                        viene dal DISEGNO, non dalle `d`
```

> **Quindi la domanda «quanti nascono sotto `LAM`», in termini relazionali, è ESATTAMENTE
> «quanti `v` stanno sotto `LAM`»** — e `_nasce` lo conta già nei contatori di `U2`
> *(`_sm_trd_mitosi` / `_sm_visd_mitosi`)*. **Qui si prende anche la DISTRIBUZIONE**, che i
> contatori non danno.

**⚠ E LO SCHWINGER NON SI AFFRANCA:** la sua `d` **è** derivata da `pos`, quindi per lui
«relazionale» **non esiste ancora**. La misura lo **mostra** invece di nasconderlo.

**Sola lettura. Nessuna cura.**
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
FUORI = os.path.join(_QUI, "_a13_relazionale")
DEST = os.path.join(FUORI, "A13_RELAZIONALE.txt")
TMP = os.path.join(FUORI, "_tmp")
os.makedirs(TMP, exist_ok=True)

SEMI = [11, 12]
SEP = 4.0
PASSI = 300

FIGLIO = r'''
import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import importlib.util as _iu
import _passo
_sp = _iu.spec_from_file_location("sim_ar", os.path.join(RAD, "soliton_simulator.py"))
S = _iu.module_from_spec(_sp); _sp.loader.exec_module(S)

S.SEMINA_LAM = True
S.SEMINA_MATURA = True
S.SCALA_MIN_PASSO = True
S.SCALA_MIN = False
S.net = S.Rete(SEME)
S.test["dati"] = {}
S._NMASSE_VIDEO["sep"] = float(SEP)
S._MC_VIDEO["nodi"] = 0
S._MC_VIDEO["fasi_casuali"] = False
S._semina_masse_coerenti()
net = S.net
LAM = float(S.LAM)

# --- L'INVOLUCRO SU `_nasce`: riceve `v` PRIMA del troncamento. Un campione per sito. ---
RACC = {}
_orig = S.Rete._nasce


def _wrap(self, v, dove="?", md=1, md0=1):
    _v = np.asarray(v, dtype=float)
    r = RACC.setdefault(dove, dict(n=0, sotto=0, somma=0.0, camp=[], minimo=float("inf"),
                                   massimo=0.0))
    if _v.size:
        r["n"] += int(_v.size)
        r["sotto"] += int(np.sum(_v < LAM))
        r["somma"] += float(_v.sum())
        r["minimo"] = min(r["minimo"], float(_v.min()))
        r["massimo"] = max(r["massimo"], float(_v.max()))
        # campione DICHIARATO: al piu' 20000 valori per sito, cosi' i quantili sono veri e la
        # memoria resta finita.
        if len(r["camp"]) < 20000:
            r["camp"].extend(_v[: 20000 - len(r["camp"])].tolist())
    return _orig(self, v, dove, md, md0)


S.Rete._nasce = _wrap

# il PASSO ZERO va escluso: la semina chiama `_nasce` per TUTTI gli archi del vuoto, e quello
#   NON e' una nascita in dinamica. Si azzera dopo la semina.
RACC.clear()

for _ in range(PASSI):
    _passo.passo_pieno(S, net)

o = dict(SEME=SEME, LAM=LAM, PASSI=int(PASSI), n_fin=int(net.n),
         nati_mitosi=int(getattr(net, "_g_nati_mitosi", 0)),
         nati_schwinger=int(getattr(net, "_g_nati_schwinger", 0)),
         siti={})
for dove, r in RACC.items():
    c = np.asarray(r["camp"], float)
    o["siti"][dove] = dict(
        n=r["n"], sotto_LAM=r["sotto"],
        frazione_sotto=float(r["sotto"] / r["n"]) if r["n"] else float("nan"),
        media=float(r["somma"] / r["n"]) if r["n"] else float("nan"),
        minimo=(float(r["minimo"]) if r["minimo"] != float("inf") else float("nan")),
        massimo=float(r["massimo"]), n_camp=int(c.size),
        p05=(float(np.percentile(c, 5)) if c.size else float("nan")),
        p50=(float(np.median(c)) if c.size else float("nan")),
        p95=(float(np.percentile(c, 95)) if c.size else float("nan")))
o["contatori_U2"] = {k: (float(v) if isinstance(v, float) else int(v))
                     for k, v in vars(net).items() if k.startswith("_sm_")}
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  siti %s  nati mitosi %d schwinger %d"
      % (NOME, sorted(RACC), o["nati_mitosi"], o["nati_schwinger"]))
'''


def braccio(seme):
    src = ("RAD = %r\nTMPD = %r\nNOME = %r\nSEME = %d\nSEP = %r\nPASSI = %d\n"
           % (RADICE, TMP, "s%d" % seme, seme, SEP, PASSI)) + FIGLIO
    p = os.path.join(TMP, "_br_s%d.py" % seme)
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    return subprocess.Popen([sys.executable, p], cwd=RADICE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


LOG = []
proc = {s: braccio(s) for s in SEMI}
for s, pr in proc.items():
    so, se = pr.communicate()
    LOG.append("[s%d] rc=%d %s" % (s, pr.returncode,
                                   (so or b"").decode("utf-8", "replace").strip()[-150:]))
    if pr.returncode:
        LOG.append((se or b"").decode("utf-8", "replace")[-1700:])

P_ = []


def P(x=""):
    P_.append(x)


P("=" * 120)
P("**`A13` ALLA NASCITA, IN MODO RELAZIONALE** — la distanza LUNGO GLI ARCHI, non su `pos`")
P("=" * 120)
P()
P("  " + _passo.descrivi())
P("  scena (ii) (b), campo MATURO, freno ON, %d passi, %d semi." % (PASSI, len(SEMI)))
P()
P("  LA CORREZIONE DI LUCA, in una riga: `pos` e' IL DISEGNO. La distanza fra due nodi e'")
P("  quella LUNGO GLI ARCHI, e il figlio nasce a `d/2` dai genitori. Quindi:")
P("     `A13` alla nascita   <=>   `d_arco >= 2 LAM`   <=>   `v >= LAM`   dove `v = d_arco/2`")
P("  cioe' **ESATTAMENTE `U2`**. Non sono due difetti: e' uno, visto da due lati.")
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
LAM = D[SEMI[0]]["LAM"]

P("-" * 120)
P("LA DISTRIBUZIONE DI `v` (la lunghezza GREZZA, prima del troncamento), per SITO")
P("-" * 120)
P("  `v` e' cio' che `_nasce` riceve. Nel sito `mitosi` vale `d_arco/2`; nel sito `schwinger`")
P("  vale `max(0.5*|pos[aa]-pos[bb]|, 0.05)` -- **cioe' viene dal DISEGNO: la voce `A3`.**")
P()
P("  %-12s %-9s %-13s %-13s %-13s %-13s %-15s"
  % ("sito", "valori", "v/LAM p05", "v/LAM p50", "v/LAM p95", "v/LAM min", "sotto LAM"))
siti = sorted({k for s in SEMI for k in D[s]["siti"]})
for dove in siti:
    def m(c):
        v = [D[s]["siti"][dove][c] for s in SEMI if dove in D[s]["siti"]]
        v = [x for x in v if x == x]
        return float(np.mean(v)) if v else float("nan")
    nn = sum(D[s]["siti"][dove]["n"] for s in SEMI if dove in D[s]["siti"])
    P("  %-12s %-9d %-13.4f %-13.4f %-13.4f %-13.4f %-15.6f"
      % (dove, nn, m("p05") / LAM, m("p50") / LAM, m("p95") / LAM, m("minimo") / LAM,
         m("frazione_sotto")))
P()
P("-" * 120)
P("`A13` ALLA NASCITA, LA RISPOSTA RELAZIONALE")
P("-" * 120)
for dove in siti:
    if dove == "semina":
        continue
    fr = [D[s]["siti"][dove]["frazione_sotto"] for s in SEMI if dove in D[s]["siti"]]
    fr = [x for x in fr if x == x]
    if not fr:
        continue
    f = float(np.mean(fr))
    nn = sum(D[s]["siti"][dove]["n"] for s in SEMI if dove in D[s]["siti"])
    P("  sito `%s`  (%d valori):" % (dove, nn))
    P("     frazione con `v < LAM`  =  %.6f      (spread fra semi %.1e)"
      % (f, (max(fr) - min(fr)) if len(fr) > 1 else float("nan")))
    P("     frazione che RISPETTA `A13`  =  %.6f" % (1.0 - f))
    if dove == "mitosi":
        P("     -> in termini relazionali: **il %.2f %% delle divisioni ha `d_arco >= 2 LAM`**"
          % (100.0 * (1.0 - f)))
        P("        e il %.2f %% NO. **Questo, e non la misura su `pos`, e' `A13` alla nascita.**"
          % (100.0 * f))
        P("        ⚠ CONFRONTO COL NUMERO GIA' NOTO: la frazione di archi sotto `2 LAM` al passo")
        P("          ZERO valeva `0.2998` (scena b). Se i due numeri differiscono, la mitosi NON")
        P("          divide a caso: **sceglie** (o evita) gli archi corti, e la differenza lo dice.")
    else:
        P("     -> ⚠ **PER LO SCHWINGER «RELAZIONALE» NON ESISTE ANCORA:** la sua `v` viene da")
        P("        `0.5*|pos[aa]-pos[bb]|`, cioè **dal DISEGNO**. E' la voce `A3`, e questa misura")
        P("        **la mostra** invece di nasconderla.")
    P()
P("-" * 120)
P("E I CONTATORI DI `U2`, che contano la STESSA COSA (controllo di coerenza)")
P("-" * 120)
for s in SEMI:
    c = D[s]["contatori_U2"]
    tr = c.get("_sm_trd_mitosi", 0)
    vi = c.get("_sm_visd_mitosi", 0)
    P("  seme %-4d `_sm_trd_mitosi`/`_sm_visd_mitosi` = %d/%d = %.6f"
      % (s, tr, vi, (tr / vi) if vi else float("nan")))
    P("           (e la stessa frazione dall'involucro: %.6f)"
      % D[s]["siti"].get("mitosi", {}).get("frazione_sotto", float("nan")))
P("  -> se le due colonne coincidono, l'involucro e i contatori misurano la stessa cosa e")
P("     nessuno dei due è sbagliato. Se differiscono, UNO DEI DUE è SBAGLIATO, e va detto.")
P()
P("COSA QUESTO NON DICE:")
P("  - DUE SEMI.")
P("  - la MISURA SU `pos` del referto precedente RESTA VALIDA **come misura del DISEGNO**: dice")
P("    che nel disegno i nati nascono sovrapposti, e quello e' un fatto sul disegno. **Non era")
P("    `A13`**, e il referto precedente va letto con questa correzione accanto.")
P("  - il campione per i quantili e' di al piu' 20000 valori per sito, DICHIARATO; `n`, `min`,")
P("    `max` e la frazione sono su TUTTI i valori.")
P("  - SOLA LETTURA. Nessuna cura.")

T = chr(10).join(P_) + chr(10)
os.makedirs(os.path.dirname(DEST), exist_ok=True)
io.open(DEST, "w", encoding="utf-8", newline="\n").write(T)
print(T)
