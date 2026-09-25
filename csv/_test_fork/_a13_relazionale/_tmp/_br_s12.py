RAD = 'C:\\Users\\lpeano\\soliton_simulator'
TMPD = 'C:\\Users\\lpeano\\soliton_simulator\\csv\\_test_fork\\_a13_relazionale\\_tmp'
NOME = 's12'
SEME = 12
SEP = 4.0
PASSI = 300

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
