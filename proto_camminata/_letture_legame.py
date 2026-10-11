# -*- coding: utf-8 -*-
r"""LE TRE MISURE DEL LEGAME — `M0` il buco, `M1` il segno, `M2` gli stati autoconsistenti.

### ⛔ **SONO OSSERVATORI, NON LEGGI:** la dinamica di default del `v3` **non cambia**, e
`soliton_simulator.py` e `leggi.yaml` **non si toccano**. ### **Le candidate `-N` e `-D` sono
ACCENDIBILI, mai di default.**

> ## ⛔ **LA REGOLA SUL RAGGIO** *(seconda versione del mandato)*: una misura di legame e'
> ## **DECIDIBILE** su una taglia solo se il **raggio** *(distanza di grafo che contiene il
> ## `90%` della norma)* e' **`< diametro/3`** ### **E** il tempo di osservazione e'
> ## **`< T_max`** *(il fronte lineare va al bordo e torna)*. ### **Altrimenti il verdetto e'
> ## `NON DECIDIBILE PER TAGLIA`.**

Soglie e previsioni: `doc/TASK_HISTORY/2026-10-11_legame.md`, **committato PRIMA** (`11b8927`).

Gira con:  python proto_camminata/_letture_legame.py
"""
import io
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

import buchi0 as B0                                            # noqa: E402
import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import camminata3 as C3                                        # noqa: E402
import geometria as GE                                         # noqa: E402
import scena as SC                                             # noqa: E402
import scene3d as S3D                                          # noqa: E402
import segni1 as S1                                            # noqa: E402
import vuoto3 as V3                                            # noqa: E402
import _letture3 as L3                                         # noqa: E402

EPS = float(np.finfo(float).eps)
SEMI = (11, 23, 37, 53)
EPS_RIF = 0.5
# ### ⛔ **LA VELOCITA- DEL FRONTE E- MISURATA, non scelta:** `0.6193` archi/tick, dal
# ### referto del `v4` *(scena regolare)*.
V_FRONTE = 0.6193
USCITE = os.path.join(_QUI, "uscite")
FONTE = os.path.join(USCITE, "letture_legame.json")


# =====================================================================================
#   LE SCENE, e la REGOLA SUL RAGGIO
# =====================================================================================
def diametro(sc, campiona=40):
    """### Il diametro: il massimo su **TUTTI** i nodi, e su `n` grande **si campiona.**

    ### ⚠ **Un diametro campionato e' un LIMITE INFERIORE**, e si dichiara come tale.
    """
    if sc["n"] <= 600:
        return max(int(SC.distanze(sc, k).max()) for k in range(sc["n"])), True
    passo = max(1, sc["n"] // campiona)
    return max(int(SC.distanze(sc, k).max())
               for k in range(0, sc["n"], passo)), False


def t_max(diam):
    """### Il tempo in cui il fronte lineare **va al bordo e torna**."""
    return int(2.0 * diam / V_FRONTE)


def raggio(sc, st, centro, frazione=0.90):
    """### La distanza di grafo che contiene il `frazione` della norma."""
    d = SC.distanze(sc, centro)
    rho = CM.rho_nodo(st["psi"], sc)
    tot = float(np.sum(rho))
    if tot <= 0:
        return float("nan")
    for r in range(0, int(d.max()) + 1):
        if float(np.sum(rho[(d >= 0) & (d <= r)])) / tot >= frazione:
            return float(r)
    return float(d.max())


def decidibile(sc, diam, rag, t_oss):
    """### La REGOLA SUL RAGGIO, applicata. ### **Ritorna il verdetto, non un `bool` muto.**"""
    ok_r = (rag == rag) and rag < diam / 3.0
    ok_t = t_oss <= t_max(diam)
    return {"raggio": rag, "diametro": diam, "raggio_su_diametro":
            (rag / diam) if diam else float("nan"),
            "soglia_raggio": diam / 3.0, "t_oss": t_oss, "t_max": t_max(diam),
            "raggio_ok": bool(ok_r), "tempo_ok": bool(ok_t),
            "decidibile": bool(ok_r and ok_t),
            "verdetto": ("DECIDIBILE" if (ok_r and ok_t)
                         else "NON DECIDIBILE PER TAGLIA")}


# ### \u26d4 **LE QUATTRO FAMIGLIE, E L-ETICHETTA DI DIMENSIONE E- MISURATA**
# ### *(rilievo del guardiano, e `scene3d.py` la misura)*: `cubico` ### **`3D`**
# ### *(`d_s ~ 3.05`)*, `geometrico3d` ### **`3D` irregolare**, `regolare` ### **`1D`**
# ### *(`d_s = 1.001`, `r2 = 1.0000`)*, `irregolare` ### **CASUALE** -- e la- `d_s`
# ### ### **CRESCE con `n`** *(`2.36` a `120`, `3.93` a `2000`)*, cioe-
# ### ### **non ha una dimensione fissa.**
def famiglia(nome):
    """### La famiglia di una scena, **dal nome**: il verdetto si riporta PER FAMIGLIA."""
    if nome.startswith("cubico"):
        return "cubico (3D)"
    if nome.startswith("geometrico3d"):
        return "geometrico3d (3D irregolare)"
    if nome.startswith("regolare"):
        return "regolare (1D)"
    return "irregolare (casuale)"


def scene_m0():
    """### Le scene di `M0`, **per famiglia**. ### **Le taglie oltre il costo NON ci sono.**"""
    return (("cubico L=5", S3D.cubico(5)),
            ("cubico L=8", S3D.cubico(8)),
            ("geometrico3d n=125", S3D.geometrico3d(125)),
            ("geometrico3d n=512", S3D.geometrico3d(512)),
            ("irregolare n=120", SC.irregolare(120)),
            ("irregolare n=500", SC.irregolare(500)),
            ("regolare n=120", SC.regolare(120)),
            ("regolare n=500", SC.regolare(500)))


def griglia_eps(sc):
    """### La griglia di `eps`: **ridotta** sulle scene grandi, e ### **si dichiara.**

    ### \u26d4 **Il motivo e' il costo CUBICO di `eig`:** a `dim > 4500` un `eps` costa
    `~170` s, e la griglia intera costerebbe ### **venti minuti per scena.** ### **Si
    tengono i tre `eps` che contano** *(`0`, `0.5`, `1`)*, e il numero dei punti
    ### **sta nelle uscite.**
    """
    return B0.EPS_GRIGLIA if 4 * sc["m"] <= 4500 else (0.0, 0.5, 1.0)


def scene_m1():
    """### Le scene di `M1`: un passo e' **lineare**, quindi ### **le taglie grandi ci sono.**"""
    return (("cubico L=5", S3D.cubico(5)),
            ("cubico L=8", S3D.cubico(8)),
            ("cubico L=12", S3D.cubico(12)),
            ("geometrico3d n=512", S3D.geometrico3d(512)),
            ("geometrico3d n=1728", S3D.geometrico3d(1728)),
            ("irregolare n=120", SC.irregolare(120)),
            ("irregolare n=2000", SC.irregolare(2000)),
            ("regolare n=120", SC.regolare(120)),
            ("regolare n=2000", SC.regolare(2000)))


# =====================================================================================
#   M0
# =====================================================================================
def m0():
    """### `M0`: i buchi su tutto il cerchio, su quattro scene e la griglia di `eps`."""
    fuori = {"griglia_eps": list(B0.EPS_GRIGLIA), "soglia_buco_in_spaziature":
             B0.SOGLIA_BUCO, "per_scena": {}, "costo_dichiarato": {}}
    for nome, sc in scene_m0():
        geo = GE.scena_identita(sc)
        diam, esatto = diametro(sc)
        per_eps = {}
        for eps in griglia_eps(sc):
            a = B0.analizza(sc, geo, eps)
            a["diametro"] = diam
            a["diametro_esatto"] = esatto
            per_eps["%g" % eps] = a
            print("    %-18s eps %-6.3f dim %-6d mult +-1 %4d/%4d  buco %.4g "
                  "(%.2f sp_u)  oltre soglia %d"
                  % (nome, eps, a["dim"], a["piu_uno"], a["meno_uno"],
                     a["senza_spigole"]["piu_grande"],
                     a["senza_spigole"]["piu_grande_in_spaziature_usati"],
                     a["senza_spigole"]["quanti_oltre_soglia"]))
        per_eps["_scena"] = {"famiglia": famiglia(nome),
                             "etichetta_dimensione": S3D.etichetta(sc["nome"]),
                             "n": sc["n"], "m": sc["m"], "diametro": diam,
                             "diametro_esatto": esatto,
                             "griglia_eps": list(griglia_eps(sc))}
        fuori["per_scena"][nome] = per_eps
    # ### il verdetto, per FAMIGLIA di scene: la taglia si confronta **dentro** la famiglia
    # ### \u26d4 **IL VERDETTO E- PER FAMIGLIA, e la conclusione sul legame vale per la
    # ### famiglia `3D`.** ### **Un buco trovato solo sull-anello si scrive <<in `1D`>>.**
    fuori["verdetti"] = {}
    for fam, pre in (("cubico (3D)", "cubico"),
                     ("geometrico3d (3D irregolare)", "geometrico3d"),
                     ("irregolare (casuale)", "irregolare"),
                     ("regolare (1D)", "regolare")):
        dentro = {k: {q: w for q, w in v.items() if q != "_scena"}
                  for k, v in fuori["per_scena"].items() if k.startswith(pre)}
        if dentro:
            fuori["verdetti"][fam] = B0.verdetto(dentro)
    # ### ⛔ **IL <<CON E SENZA VUOTO>>, misurato UNA VOLTA e dichiarato:** il passo lineare
    # ### `v2` ### **non legge `phi`** -- e si prova ### **sul sorgente E al bit.**
    sc = SC.irregolare(120)
    geo = GE.scena_identita(sc)
    uno = np.ones(sc["n"], dtype=float)
    st = C3.stato3(sc, 11)
    a = st["psi"].copy()
    b = dict(st)
    for _ in range(20):
        a = C2.passo2(a, sc, geo, uno, 1.0, EPS_RIF)
        b = C3.passo3(b, sc, geo, uno, 1.0, EPS_RIF, None)
    src = io.open(os.path.join(_QUI, "camminata2.py"), encoding="utf-8").read()
    corpo = src.split("def passo2(")[1].split("def corri2(")[0]
    fuori["vuoto_non_tocca_lo_spinore"] = {
        "scarto_al_bit": float(np.max(np.abs(b["psi"] - a))),
        "phi_nel_passo_lineare": ("phi" in corpo),
        "nota": "il passo lineare v2 non prende phi fra gli argomenti e non lo nomina nel "
                "corpo: lo spettro dello spinore NON PUO- dipendere dal vuoto, e il bit lo "
                "conferma"}
    return fuori


# =====================================================================================
#   M1
# =====================================================================================
def m1():
    """### `M1`: la lettura `T` del `v3` per `+N`, `-N`, `+D`, `-D` e il **lineare**.

    ### ⛔ **LE SOGLIE SONO QUELLE DEL `v3`, RICOPIATE:** la frazione di norma entro **UN
    ARCO** dal centro contro il **fondo uniforme**, e *«piu' concentrato del lineare»* vuol
    dire ### **oltre `3 sigma`** sui `4` semi. ### **Se le cambiassi, il confronto col `v3`
    non vorrebbe dire niente.**
    """
    fuori = {"griglia_x0": list(S1.X0_GRIGLIA), "per_scena": {}}
    for nome, sc in scene_m1():
        geo = GE.scena_identita(sc)
        diam, esatto = diametro(sc)
        t_oss = min(40, t_max(diam))
        per_var = {}
        for et in S1.VARIANTI:
            fl = S1.flusso_di(et)
            per_x0 = {}
            for x0 in S1.X0_GRIGLIA:
                fr, fo, rr = [], [], []
                for s in SEMI:
                    st, dentro, d = L3.grumo(sc, geo, 0, 1, x0, seme=s)
                    z = dict(st)
                    for _ in range(t_oss):
                        z = C3.passo3(z, sc, geo, np.ones(sc["n"]), 1.0, EPS_RIF, fl)
                    fr.append(L3.frazione_entro(sc, z, 0, d, 1))
                    fo.append(L3.fondo_uniforme(sc, d, 1))
                    rr.append(raggio(sc, z, 0))
                    del dentro
                rap = [a / b for a, b in zip(fr, fo)]
                reg = decidibile(sc, diam, float(np.mean(rr)), t_oss)
                per_x0["%g" % x0] = {
                    "x0": x0, "rapporto": float(np.mean(rap)),
                    "sigma": (float(np.std(rap, ddof=1)) / math.sqrt(len(rap))
                              if len(rap) > 1 else 0.0),
                    "frazione": float(np.mean(fr)), "fondo": float(np.mean(fo)),
                    "raggio": float(np.mean(rr)), "regola": reg, "semi": len(SEMI)}
            per_var[et] = per_x0
        # ### il confronto col LINEARE, con il `sigma` COMBINATO
        for et in S1.VARIANTI:
            if et == "lineare":
                continue
            for k in per_var[et]:
                a = per_var[et][k]
                b = per_var["lineare"][k]
                sg = math.sqrt(a["sigma"] ** 2 + b["sigma"] ** 2)
                dd = a["rapporto"] - b["rapporto"]
                a["contro_lineare"] = {
                    "differenza": dd, "sigma_combinato": sg,
                    "in_sigma": (abs(dd) / sg) if sg > 0 else 0.0,
                    "piu_concentrato": bool(dd > 3.0 * sg and sg > 0.0),
                    "decidibile": a["regola"]["decidibile"]}
        per_var["_scena"] = {"diametro": diam, "diametro_esatto": esatto,
                             "t_oss": t_oss, "t_max": t_max(diam),
                             "n": sc["n"], "m": sc["m"],
                             "famiglia": famiglia(nome),
                             "etichetta_dimensione": S3D.etichetta(sc["nome"])}
        fuori["per_scena"][nome] = per_var
        decid = [k for et in S1.VARIANTI if et != "lineare"
                 for k, v in per_var[et].items()
                 if v.get("contro_lineare", {}).get("decidibile")]
        vinti = [(et, k) for et in S1.VARIANTI if et != "lineare"
                 for k, v in per_var[et].items()
                 if v.get("contro_lineare", {}).get("piu_concentrato")
                 and v["regola"]["decidibile"]]
        print("    %-18s diam %-4s t_oss %-4d  casi DECIDIBILI %-4d  piu- concentrati "
              "del lineare: %s"
              % (nome, ("%d" % diam) if esatto else (">=%d" % diam), t_oss,
                 len(decid), vinti or "NESSUNO"))
    return fuori


# =====================================================================================
def main():
    SC._niente_simulatore()
    os.makedirs(USCITE, exist_ok=True)
    fuori = {"velocita_del_fronte_misurata": V_FRONTE, "semi": list(SEMI),
             "eps_del_passo": EPS_RIF}
    print("=" * 100)
    print("LE TRE MISURE DEL LEGAME")
    print("=" * 100)
    # ### \u26d4 **PRIMA DI TUTTO LE DIMENSIONI, perche- decidono come si legge il resto**
    print("  --- le DIMENSIONI SPETTRALI, misurate ---")
    fuori["dimensioni"] = {}
    for nome, sc in (("cubico L=5", S3D.cubico(5)), ("cubico L=8", S3D.cubico(8)),
                     ("cubico L=12", S3D.cubico(12)), ("cubico L=20", S3D.cubico(20)),
                     ("geometrico3d n=512", S3D.geometrico3d(512)),
                     ("geometrico3d n=4000", S3D.geometrico3d(4000)),
                     ("regolare n=120", SC.regolare(120)),
                     ("regolare n=2000", SC.regolare(2000)),
                     ("irregolare n=120", SC.irregolare(120)),
                     ("irregolare n=2000", SC.irregolare(2000))):
        diam, esatto = diametro(sc)
        ds = S3D.dimensione_spettrale(
            sc, diam, semi_nodi=(0, sc["n"] // 3, sc["n"] // 2))
        ds.update({"famiglia": famiglia(nome), "etichetta": S3D.etichetta(sc["nome"]),
                   "n": sc["n"], "m": sc["m"], "diametro": diam,
                   "diametro_esatto": esatto,
                   "gradi": [int(sc["grado"].min()), int(sc["grado"].max())]})
        fuori["dimensioni"][nome] = ds
        print("    %-22s %-16s n %-6d diametro %-5d d_s %-7.3f r2 %.4f  %s"
              % (nome, ds["etichetta"], sc["n"], diam, ds["d_s"], ds["r2"],
                 "potenza" if ds["potenza"] else "### NESSUNA potenza"))
    print("  --- M0: i buchi su tutto il cerchio ---")
    fuori["M0"] = m0()
    for fam, v in fuori["M0"]["verdetti"].items():
        print("  ### VERDETTO M0 %-32s %s" % (fam, v["verdetto"]))
    print("  --- M1: il segno della saturazione ---")
    fuori["M1"] = m1()
    io.open(FONTE, "wb").write(
        (json.dumps(fuori, ensure_ascii=False, indent=1, sort_keys=True)
         + chr(10)).encode("utf-8"))
    print("-" * 100)
    print("  scritto %s" % os.path.relpath(FONTE, RADICE).replace(os.sep, "/"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
