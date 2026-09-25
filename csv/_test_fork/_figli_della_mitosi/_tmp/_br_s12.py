RAD = 'C:\\Users\\lpeano\\soliton_simulator'
TMPD = 'C:\\Users\\lpeano\\soliton_simulator\\csv\\_test_fork\\_figli_della_mitosi\\_tmp'
NOME = 's12'
SEME = 12
SEP = 4.0
PASSI = 300
ISTANTI = [1, 5, 20, 60, 120, 200, 300]

import io, json, os, sys
import numpy as np
from scipy.spatial import cKDTree
sys.path.insert(0, RAD)
sys.path.insert(0, os.path.join(RAD, "csv"))
import importlib.util as _iu
import _passo
_sp = _iu.spec_from_file_location("sim_fm", os.path.join(RAD, "soliton_simulator.py"))
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
n0 = int(net.n)

# ---- MISURA 1: l'involucro su `mitosi`, che guarda ALLE POSIZIONI DI NASCITA ----------------
NASCITE = []
_orig_mit = S.Rete.mitosi


def _wrap_mit(self):
    _n_pre = int(self.n)
    _mit_pre = int(getattr(self, "_g_nati_mitosi", 0))
    _sch_pre = int(getattr(self, "_g_nati_schwinger", 0))
    _fuori = _orig_mit(self)
    _n_post = int(self.n)
    if _n_post > _n_pre:
        _pos = np.asarray(self.pos, float)
        _nuovi = np.arange(_n_pre, _n_post)
        # LA DISTANZA DAL PIU' VICINO FRA TUTTI: `k=2` perche' il primo vicino e' se stesso
        _T = cKDTree(_pos)
        _dd = _T.query(_pos[_nuovi], k=2)[0][:, 1]
        _d_mit = int(getattr(self, "_g_nati_mitosi", 0)) - _mit_pre
        _d_sch = int(getattr(self, "_g_nati_schwinger", 0)) - _sch_pre
        # il canale si distingue dai CONTATORI, non dall'ordine: i figli della divisione
        # vengono prima, gli antinodi Schwinger dopo. E se i conti non tornano, SI DICHIARA.
        _canale = (["mitosi"] * min(_d_mit, len(_nuovi))
                   + ["schwinger"] * max(0, len(_nuovi) - _d_mit))
        _quadra = bool(_d_mit + _d_sch == len(_nuovi))
        # il grado ALLA NASCITA
        _g = np.zeros(_n_post, int)
        _ii = np.asarray(self.i, int); _jj = np.asarray(self.j, int)
        _m = (_ii < _n_post) & (_jj < _n_post)
        np.add.at(_g, _ii[_m], 1); np.add.at(_g, _jj[_m], 1)
        for _k, _idx in enumerate(_nuovi):
            NASCITE.append(dict(nodo=int(_idx), passo=int(PASSO[0]),
                                dist_min=float(_dd[_k]), dist_su_LAM=float(_dd[_k] / LAM),
                                canale=(_canale[_k] if _k < len(_canale) else "?"),
                                grado_nascita=int(_g[_idx]), quadra=_quadra,
                                d_mit=_d_mit, d_sch=_d_sch, nuovi=int(len(_nuovi))))
    return _fuori


S.Rete.mitosi = _wrap_mit
PASSO = [0]

# ---- MISURA 2: la traiettoria dei nati -----------------------------------------------------
TRAI = []


def _istantanea(net, passo):
    n = int(net.n)
    om = np.linalg.norm(np.asarray(net.omega_s, float), axis=1) if np.size(net.omega_s) \
        else np.zeros(n)
    om = om[:n] if om.size >= n else np.pad(om, (0, n - om.size))
    rho = np.asarray(net._rho_sorgente(), float)
    rho = rho[:n] if rho.size >= n else np.pad(rho, (0, n - rho.size))
    g = np.zeros(n, int)
    ii = np.asarray(net.i, int); jj = np.asarray(net.j, int)
    m = (ii < n) & (jj < n)
    np.add.at(g, ii[m], 1); np.add.at(g, jj[m], 1)
    nati = np.arange(n0, n)
    o = dict(passo=int(passo), n=n, nati=int(nati.size))
    for et, sel in (("nati", nati), ("orig", np.arange(min(n0, n)))):
        if not sel.size:
            continue
        o["grado_%s_p50" % et] = float(np.median(g[sel]))
        o["grado_%s_max" % et] = float(g[sel].max())
        o["grado_%s_fraz2" % et] = float(np.mean(g[sel] == 2))
        o["rho_%s_p50" % et] = float(np.median(rho[sel]))
        o["om_%s_p50" % et] = float(np.median(om[sel]))
        o["om_%s_max" % et] = float(om[sel].max())
    o["al_pavimento_cum"] = int(getattr(net, "_inerzia_al_pavimento", 0))
    o["inerzia_tot_cum"] = int(getattr(net, "_inerzia_tot", 0))
    return o


TRAI.append(_istantanea(net, 0))
for k in range(1, PASSI + 1):
    PASSO[0] = k
    _passo.passo_pieno(S, net)
    if k in ISTANTI:
        TRAI.append(_istantanea(net, k))

out = dict(SEME=SEME, LAM=LAM, n0=n0, n_fin=int(net.n), PASSI=int(PASSI),
           nascite=NASCITE, traiettoria=TRAI,
           frazione_archi_sotto_2lam_ini=None)
io.open(os.path.join(TMPD, NOME + ".json"), "w", encoding="utf-8").write(json.dumps(out))
print("OK %s  n %d -> %d  nascite registrate %d" % (NOME, n0, net.n, len(NASCITE)))
