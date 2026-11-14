# -*- coding: utf-8 -*-
r"""**IL BILANCIO DELLE ENERGIE: I PEZZI** *(Luca `2026-11-13` `23:47`, la voce `15`; la carta `doc/TASK_HISTORY/2026-11-14_bilancio_energie.md`; R-CONTI)*.

### **Le definizioni sono quelle ESISTENTI** *(nessuna nuova)*: **i conti per nodo** *(`_libro_dei_conti.conti_per_nodo`: `cost`, `cin`, `leg`, `vuo`, `tot`, `M`, `V`)*, **`K + V` del campo**
*(`Campo.K() + Campo.V()`)*. ### **I pezzi B1:** **(a) la materia `cost + cin + leg` per solitone** *(i nodi entro `R_PEZZO` dal centro del solitone PIU' VICINO)* **e fuori; (b) il moto: la
velocita' del centro e la STIMA `M_in v^2 / 2`** *(IPOTESI dichiarata: `M_in = -mu M`, `mu = 1/|eps''|`, NEGATIVA)*; **(c) `K + V`; (d) il vuoto `vuo` per solitone e lontano; (e) il bordo**
*(la massa e `tot` prima e dopo `bordo.assorbi`)*; **(f) il residuo.** ### **I pezzi per regione dipendono dallo zero** *(dichiarato; si leggono le variazioni)*.
### **La somma dei pezzi = il totale ESATTA** *(in aritmetica razionale: `fractions.Fraction`; la divisione non perde niente)*.
**`scena(corsa, t)`: COPIATA da `mattone.scena`** *(ramo `strumento-mattone`; qui serve sul principale)*.
"""
import contextlib
import fractions
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import solitone  # noqa: E402,F401  (i percorsi)

R_PEZZO = 28.0           # ### il raggio dei pezzi per solitone: il R_t di TBS a 10000 (il francobollo del mattone), dichiarato
TERMINI_MATERIA = ("cost", "cin", "leg")


@contextlib.contextmanager
def scena(corsa, t_stato):
    """### **La scena di una corsa** *(COPIATA da `mattone.scena`)*: `Z` con lo stato a `t_stato`, il bordo, la fase del vuoto, `e_K`; `Z["metti"](stato)`."""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    sol, vuoto, s = V.CORSE[CA.NOME]
    T_acc, _f = CA.CORSE[corsa]
    K = int(round(T_acc / s))
    rr = CA.serie(corsa)[0]
    x_st = [x for r in rr for x in (r.get("stati") or []) if x["t"] == t_stato]
    assert len(x_st) == 1, "lo stato di %s a %d NON e' uno solo" % (corsa, t_stato)
    bor = rr[-1]["bordo"]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
        assert int(d["K"]) == K
    with CA.con_L(CA.LCORSA.get(corsa)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, rec["larghezza"])[0]
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, corsa)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot = z["st"], z["mot"]
        n, L = z["inc"].n, z["L"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        cs0, lc0 = mot.cs, getattr(mot, "lambda_c", None)
        U0 = mot.geo.U.copy()
        with np.load(x_st[0]["file"]) as d:
            stato = {k: d[k].copy() for k in chiavi}

        def metti(st_dato=None):
            for k in chiavi:
                st[k][...] = (st_dato or stato)[k]
            mot.cs, mot.lambda_c = cs0, lc0
            mot.geo.U[...] = U0
        metti()
        assert V.shas(z) == x_st[0]["sha"], "lo stato di %s a %d NON e' quello registrato" % (corsa, t_stato)
        v_ = np.arange(n)
        g_e = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])[0]
        Z = {"z": z, "st": st, "mot": mot, "par": z["par"], "n": n, "L": L, "nodo": np.asarray(z["inc"].nodo), "m1": v_ // L, "m2": v_ % L, "chiavi": chiavi,
             "stato": stato, "metti": metti, "phi_v": phi_v, "tab_c": tab_c, "omega": omega, "K": K, "s": s, "e_K": e_K, "g_e": g_e, "bordo": bor, "U0": U0, "w_in": w_in}
        try:
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                yield Z
        finally:
            metti()


def conti_nodo(Z):
    import _libro_dei_conti as LC
    import _vuoto_vivo_B as V
    return LC.conti_per_nodo(Z["z"]["inc"], Z["mot"], Z["st"], Z["e_K"], V.LAM_ZERO, Z["par"])


def totale(Z):
    """### `tot` del toro, come `p6_bracci` *(`np.sum` dei conti per nodo)*."""
    return float(np.sum(conti_nodo(Z)["tot"]))


def etichette(Z, centri):
    """### **Ogni nodo a un pezzo:** `i` = il solitone `i` *(il centro piu' vicino, se entro `R_PEZZO`)*, `-1` fuori. **Una PARTIZIONE dei nodi.**"""
    from solitone import toro as TO
    dd = np.stack([np.hypot(*TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"]).T[:2]) for c in centri])
    vic = np.argmin(dd, axis=0)
    return np.where(dd[vic, np.arange(Z["n"])] <= R_PEZZO, vic, -1)


def esatta(x):
    """### La somma ESATTA di un array di float *(razionale)*."""
    return sum((fractions.Fraction(float(v)) for v in np.asarray(x).ravel()), fractions.Fraction(0))


def pezzi(Z, centri, campo):
    """### **I pezzi B1 di uno stato** *(senza il moto: vuole due stati)*: `{"materia": [per solitone] + [fuori], "vuoto": [...], "KV", "tot", "M", "V", "somma_esatta_ok"}`."""
    c = conti_nodo(Z)
    lab = etichette(Z, centri)
    nn = len(centri)
    out = {"materia": [], "vuoto": [], "massa": []}
    for i in list(range(nn)) + [-1]:
        m = lab == i
        out["materia"].append(float(sum(np.sum(c[k][m]) for k in TERMINI_MATERIA)))
        out["vuoto"].append(float(np.sum(c["vuo"][m])))
        out["massa"].append(float(np.sum(c["M"][m])))
    out["KV"] = (campo.K() + campo.V()) if campo is not None else 0.0
    out["tot"] = float(np.sum(c["tot"]))
    out["M"], out["V"] = float(np.sum(c["M"])), float(np.sum(c["V"]))
    # ### la divisione non perde niente: la somma ESATTA dei pezzi (materia + vuoto, per etichetta) = la somma ESATTA di tot
    pezzi_esatti = sum((esatta(c[k][lab == i]) for i in list(range(nn)) + [-1] for k in TERMINI_MATERIA + ("vuo",)), fractions.Fraction(0))
    out["somma_esatta_ok"] = pezzi_esatti == esatta(c["cost"]) + esatta(c["cin"]) + esatta(c["leg"]) + esatta(c["vuo"])
    out["tot_meno_pezzi"] = float(esatta(c["tot"]) - pezzi_esatti)      # ### tot = em + vuo + leg = cost + cin + vuo + leg in float: la differenza di arrotondamento, scritta
    return out


def moto(c_prima, c_dopo, dt, L, massa, mu):
    """### **(b) il moto:** la velocita' del centro *(lo scarto periodico / `dt`)* e la STIMA `M_in v^2 / 2`, `M_in = -mu massa` *(IPOTESI, dichiarata)*."""
    from solitone import toro as TO
    p = TO.scarti(np.array([c_dopo[0]]), np.array([c_dopo[1]]), c_prima[0], c_prima[1], L)[0]
    v = float(np.hypot(p[0], p[1])) / dt
    return v, -mu * massa * v * v / 2.0
