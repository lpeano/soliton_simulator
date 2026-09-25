RAD = 'C:\\Users\\lpeano\\soliton_simulator'
TMPD = 'C:\\Users\\lpeano\\soliton_simulator\\csv\\_test_fork\\_limite_accoppiamento\\_tmp'
NOME = 's12'
SEME = 12
SEP = 4.0
COPIA = 'C:\\Users\\lpeano\\soliton_simulator\\csv\\_test_fork\\_limite_accoppiamento\\_sim_diag.py'
GRADI = [77, 20, 8, 4, 2]
PASSI_PRIMA = 20

import io, json, os, sys
import numpy as np
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import importlib.util as _iu
import _passo
_sp = _iu.spec_from_file_location("sim_la", COPIA)
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
# il campo deve ESISTERE: `PASSI_PRIMA` passi PIENI prima di operare
for _ in range(PASSI_PRIMA):
    _passo.passo_pieno(S, net)

n = int(net.n)
ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
grado = np.zeros(n, int)
m = (ii < n) & (jj < n)
np.add.at(grado, ii[m], 1); np.add.at(grado, jj[m], 1)
# IL NODO BERSAGLIO: uno NORMALE, cioe' col grado piu' vicino alla MEDIANA. Non il massimo,
# non il minimo: la domanda e' sul limite, e il punto di partenza deve essere tipico.
gm = int(np.median(grado))
cand = np.where(grado == gm)[0]
if not cand.size:
    cand = np.array([int(np.argmin(np.abs(grado - gm)))])
BERS = int(cand[0])

# IL TAGLIO: si TOLGONO archi del bersaglio fino a `K`. Si tolgono gli archi PIU' LUNGHI per
#   primi -- una scelta, e la dichiaro: togliere i piu' CORTI cambierebbe il vicinato piu'
#   vicino, che e' quello che pesa di piu' nel kernel `exp(-d/lam)`. Togliere i piu' lunghi
#   e' il taglio MENO invasivo a parita' di `k`.
d = np.asarray(net.d, float)
suoi = np.where((ii == BERS) | (jj == BERS))[0]
ordine_tagli = suoi[np.argsort(d[suoi])[::-1]]     # dal piu' LUNGO al piu' corto

o = dict(SEME=SEME, n=n, bersaglio=BERS, grado_iniziale=int(grado[BERS]),
         grado_mediano=gm, archi_suoi=int(suoi.size), casi=[])

for K in GRADI:
    if K > suoi.size:
        o["casi"].append(dict(K=int(K), salta="il bersaglio ha solo %d archi" % suoi.size))
        continue
    # UNA COPIA DELLA RETE per caso: si ricostruisce da zero e si rifa' il taglio, cosi' i
    # casi sono INDIPENDENTI (non si tagliano a cascata sullo stesso oggetto).
    import copy as _copy
    net2 = _copy.deepcopy(net)
    quanti = int(suoi.size - K)
    via = set(int(x) for x in ordine_tagli[:quanti])
    keep = np.array([k not in via for k in range(len(net2.d))], bool)
    for _nome in ("i", "j", "d", "d0", "vd", "tw", "twp", "eta_arco"):
        _v = getattr(net2, _nome, None)
        if isinstance(_v, np.ndarray) and _v.shape[0] == keep.size:
            setattr(net2, _nome, _v[keep])
    for _nome in list(vars(net2)):
        _v = getattr(net2, _nome)
        if isinstance(_v, np.ndarray) and _v.ndim >= 1 and _v.shape[0] == keep.size \
                and _nome not in ("i", "j", "d", "d0"):
            setattr(net2, _nome, _v[keep])
    net2._S = None; net2._perm = None; net2._ker_cache = None
    net2._cicli_topologici = None
    # UN passo PIENO, e si leggono i diagnostici
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
        c = dict(K=int(K), grado_vero=int(_g[BERS]) if BERS < _g.size else -1,
                 archi_tolti=quanti, archi_rimasti=int(keep.sum()))
        if _in.size > BERS:
            c["inerzia"] = float(_in[BERS])
            c["al_pavimento"] = bool(_in[BERS] <= 1e-6)
        if _ct.size > BERS:
            c["contrasto"] = float(_ct[BERS])
        if _t2.size > BERS:
            c["T2"] = float(_t2[BERS])
        if _co.size > BERS:
            c["coppia"] = float(np.linalg.norm(_co[BERS]))
        if _om.size > BERS:
            c["omega"] = float(_om[BERS])
        if "coppia" in c and "inerzia" in c and c["inerzia"]:
            c["coppia_su_inerzia"] = c["coppia"] / c["inerzia"]
        o["casi"].append(c)
    except Exception as e:
        o["casi"].append(dict(K=int(K), errore=str(e)[:160]))

io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(o))
print("OK %s  bersaglio %d (grado %d), casi %d" % (NOME, BERS, o["grado_iniziale"],
                                                   len(o["casi"])))
