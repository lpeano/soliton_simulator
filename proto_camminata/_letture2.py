# -*- coding: utf-8 -*-
"""LE NOVE LETTURE DEL `v2` — **i numeri, e le soglie sono quelle del task history.**

> ### ⛔ **NIENTE SI DECIDE QUI:** criteri, previsioni e soglie stanno in
> `doc/TASK_HISTORY/2026-10-10_prototipo_camminata_v2.md`, **committato prima del codice**.

| | la lettura | che cosa misura |
|---|---|---|
| `G` | **GAUGE** | le osservabili invarianti del gauge puro **contro** l'identita' |
| `G!` | ### ⛔ **DEVE FALLIRE** | lo stesso gauge **coi versori NON ruotati** |
| `1` | **ISOTROPIA** | rinumerazione **che porta i versori e le `U`** |
| `2` | **CONO** | zero esatto oltre un arco per tick |
| `B` | **BANDE ACCOPPIATE** | quanta ampiezza passa all'altra componente, al variare di `eps` |
| `M` | **MASSA O NO** | il **gap** nello spettro di quasi-energia |
| `3` | **QUANTITA' CONSERVATA** | quattro candidate, `4` semi, con la **risoluzione** prima della statistica |
| `4` | **CLUSTER** | dispersione pesata e frazione intrappolata |
| `5` | **MATERIA / ANTIMATERIA** | il cluster e il suo **coniugato `C`** — ### **e adesso e' una prova FISICA** |
| `O` | **OLONOMIA** | le olonomie **non cambiano** durante la corsa *(controllo)* |

Gira con:  python proto_camminata/_letture2.py
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

import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import geometria as GE                                         # noqa: E402
import nonlineare2 as N2                                       # noqa: E402
import scena as SC                                             # noqa: E402
import _letture as L1                                          # noqa: E402

EPS = float(np.finfo(float).eps)
NLN = chr(10)
USCITE = os.path.join(_QUI, "uscite")
SEMI = (11, 23, 37, 53)
PASSI_LUNGHI = 200
PASSI_CORTI = 40
EPS_RIF = 0.5


def porta_geometria(geo, sc, mappa, pa_segno):
    """### La geometria **PORTATA** sulla scena rinumerata.

    ### ⛔ **I versori NON si rigenerano: si PORTANO.** Rigenerarli darebbe
    ### **un'altra scena**, e la lettura `1` misurerebbe **due scene diverse** invece
    dell'isotropia. ### ⚠ **E se un arco si e' RIGIRATO, la sua `U` va CONIUGATA.**
    """
    n2 = np.zeros_like(geo["n"])
    n2[mappa] = geo["n"]
    U2 = np.zeros_like(geo["U"])
    for a_vecchio, (a_nuovo, girato) in enumerate(pa_segno):
        U2[a_nuovo] = geo["U"][a_vecchio].conj().T if girato else geo["U"][a_vecchio]
    return {"nome": geo["nome"] + "+portata", "U": U2, "n": n2, "come": geo["come"]}


def mappa_archi(sc, nuova, mappa):
    """### `[(arco nuovo, e- girato?)]` per ogni arco vecchio, dalla mappa delle estremita'."""
    fuori = []
    for a in range(sc["m"]):
        e_nuovo = int(mappa[2 * a])
        fuori.append((e_nuovo // 2, e_nuovo % 2 == 1))
    return fuori


def cluster2(sc, seme, banda=0):
    return L1.cluster(sc, seme, banda)


def profilo2(sc, geo, r, dt, eps, seme, g, f, passi, banda=0):
    """Una corsa del `v2`, con le stesse letture del `v1`."""
    psi, dentro = cluster2(sc, seme, banda)
    serie = {nome: [] for nome, _fn in CANDIDATE}
    disp, intr, tempo = [], [], []
    prec = psi
    for t in range(1, passi + 1):
        nuovo = C2.passo2(prec, sc, geo, r, dt, eps, g, f)
        if t % 4 == 0 or t == passi:
            om, peso = L1.frequenze(sc, prec, nuovo)
            disp.append(L1.dispersione(om, peso, dentro))
            intr.append(L1.intrappolata(sc, nuovo, dentro))
            tempo.append(t)
            for nome, fn in CANDIDATE:
                serie[nome].append(fn(nuovo, sc, geo, r, dt, eps, g, f))
        prec = nuovo
    return {"tempo": tempo, "dispersione": disp, "intrappolata": intr, "serie": serie,
            "dentro": dentro, "fine": prec}


# =====================================================================================
#   LE CANDIDATE -- dichiarate
# =====================================================================================
def _c_norma(psi, sc, geo, r, dt, eps, g, f):
    return CM.norma(psi)


def _c_quasi(psi, sc, geo, r, dt, eps, g, f):
    u = C2.passo2(psi, sc, geo, r, dt, eps, g, f)
    return float(np.real(np.sum(np.conj(psi) * u)))


def _c_energia_rho(psi, sc, geo, r, dt, eps, g, f):
    u = C2.passo2(psi, sc, geo, r, dt, eps)
    lin = float(np.real(np.sum(np.conj(psi) * u)))
    return lin + 0.5 * g * float(np.sum(CM.rho_nodo(psi, sc) ** 2 * r * dt))


def _c_energia_elicita(psi, sc, geo, r, dt, eps, g, f):
    u = C2.passo2(psi, sc, geo, r, dt, eps)
    lin = float(np.real(np.sum(np.conj(psi) * u)))
    h = N2.elicita_nodo(psi, sc, geo)
    return lin + 0.5 * g * float(np.sum(h ** 2 * r * dt))


CANDIDATE = (
    ("la norma", _c_norma),
    ("la quasi-energia del passo", _c_quasi),
    ("energia + termine su rho", _c_energia_rho),
    ("energia + termine sull-elicita", _c_energia_elicita),
)


def main():
    SC._niente_simulatore()
    os.makedirs(USCITE, exist_ok=True)
    sc = SC.irregolare()
    r = SC.ritmi(sc, SEMI[0])
    psi = CM.stato_casuale(sc, SEMI[0])
    gmax = int(sc["grado"].max())
    nest = 2 * sc["m"]
    ident = GE.scena_identita(sc)
    gauge = GE.scena_gauge_puro(sc, SEMI[0])
    curva = GE.scena_curva(sc, SEMI[0])
    SCENE = (("identita", ident), ("gauge_puro", gauge), ("curva", curva))
    tol = PASSI_CORTI * gmax * EPS * math.sqrt(CM.norma(psi))
    out = {"scena": {"nome": sc["nome"], "n": sc["n"], "archi": sc["m"],
                     "estremita": nest, "gradi": sorted(set(sc["grado"].tolist())),
                     "semi": list(SEMI), "eps_riferimento": EPS_RIF,
                     "passi_lunghi": PASSI_LUNGHI, "passi_corti": PASSI_CORTI},
           "letture": {}}
    print("=" * 100)
    print("LE NOVE LETTURE DEL PROTOTIPO v2")
    print("=" * 100)
    print("  scena: %s   estremita-: %d   soglia S1 = %.3g" % (sc["nome"], nest, tol))

    # ================================================================ G e G!
    def ruota(p, g, fi):
        o = np.empty_like(p)
        for e in range(p.shape[0]):
            k = int(sc["nodo"][e])
            o[e] = np.exp(1j * fi[k]) * (g[k] @ p[e])
        return o

    ruot = ruota(psi, gauge["g"], gauge["fi"])
    f_i, _ = C2.corri2(psi, sc, ident, r, 1.0, EPS_RIF, PASSI_CORTI)
    f_g, _ = C2.corri2(ruot, sc, gauge, r, 1.0, EPS_RIF, PASSI_CORTI)
    senza = dict(gauge)
    senza["n"] = gauge["n_non_ruotati"]
    f_s, _ = C2.corri2(ruot, sc, senza, r, 1.0, EPS_RIF, PASSI_CORTI)
    d_rho = float(np.max(np.abs(CM.rho_nodo(f_i, sc) - CM.rho_nodo(f_g, sc))))
    d_bad = float(np.max(np.abs(CM.rho_nodo(f_i, sc) - CM.rho_nodo(f_s, sc))))
    ol_i = GE.olonomie(sc, ident["U"])
    ol_g = GE.olonomie(sc, gauge["U"])
    d_ol = max(abs(a[1] - b[1]) + abs(a[2] - b[2]) for a, b in zip(ol_i, ol_g))
    om_i, _ = C2.quasi_energie(sc, ident, r, 1.0, EPS_RIF)
    om_g, _ = C2.quasi_energie(sc, gauge, r, 1.0, EPS_RIF)
    d_sp = float(np.max(np.abs(om_i - om_g)))
    out["letture"]["G_gauge"] = {"densita": d_rho, "olonomie": d_ol, "spettro": d_sp,
                                 "soglia": tol}
    out["letture"]["G_deve_fallire"] = {"densita_senza_ruotare_versori": d_bad}
    print("  G   densita- %.3g   olonomie %.3g   spettro %.3g   (soglia %.3g)"
          % (d_rho, d_ol, d_sp, tol))
    print("  G!  coi versori NON ruotati: %.3g   ### deve essere GRANDE" % d_bad)

    # ================================================================ 1 isotropia
    nuova, pn, mappa = SC.rinumera(sc, 23)
    rn = np.empty_like(r)
    rn[pn] = r
    pas = mappa_archi(sc, nuova, mappa)
    iso = {}
    for nome, geo in SCENE:
        g2 = porta_geometria(geo, sc, mappa, pas)
        f1, _ = C2.corri2(psi, sc, geo, r, 1.0, EPS_RIF, PASSI_CORTI)
        pp = np.zeros_like(psi)
        pp[mappa] = psi
        f2, _ = C2.corri2(pp, nuova, g2, rn, 1.0, EPS_RIF, PASSI_CORTI)
        rip = np.zeros_like(f2)
        rip[mappa] = f1
        iso[nome] = float(np.max(np.abs(rip - f2)))
    iso["soglia"] = tol
    out["letture"]["1_isotropia"] = iso
    print("  1   isotropia: %s   (soglia %.3g)"
          % ("  ".join("%s %.3g" % (k, v) for k, v in iso.items() if k != "soglia"), tol))

    # ================================================================ 2 cono
    d0 = SC.distanze(sc, 0)
    T = max(1, int(d0.max()) // 2)
    e0 = int(np.nonzero(sc["nodo"] == 0)[0][0])
    u1 = CM.stato_zero(sc)
    u1[e0, 0] = 1.0
    u2 = u1.copy()
    u2[e0, 0] = 1.0 + 1e-3
    cono = {}
    for nome, geo in SCENE:
        g1, _ = C2.corri2(u1, sc, geo, r, 1.0, EPS_RIF, T)
        g2, _ = C2.corri2(u2, sc, geo, r, 1.0, EPS_RIF, T)
        dif = np.abs(g1 - g2).sum(axis=1)
        fu = dif[d0[sc["nodo"]] > T]
        cono[nome] = float(np.max(fu)) if fu.size else -1.0
    cono["T"] = T
    cono["estremita_fuori"] = int(np.sum(d0[sc["nodo"]] > T))
    out["letture"]["2_cono"] = cono
    print("  2   cono (T=%d, %d estremita- fuori): %s" % (
        T, cono["estremita_fuori"],
        "  ".join("%s %.3g" % (k, v) for k, v in cono.items()
                  if k not in ("T", "estremita_fuori"))))

    # ================================================================ B bande
    solo0 = psi.copy()
    solo0[:, 1] = 0.0
    solo0 = solo0 / math.sqrt(CM.norma(solo0))
    bande = {}
    for nome, geo in SCENE:
        per_eps = {}
        for eps in N2.EPS_SCANSIONE:
            f, _ = C2.corri2(solo0, sc, geo, r, 1.0, eps, PASSI_CORTI)
            per_eps["%g" % eps] = float(np.sum(np.abs(f[:, 1]) ** 2))
        bande[nome] = per_eps
    out["letture"]["B_bande"] = bande
    print("  B   peso nella componente 1 dopo %d tick:" % PASSI_CORTI)
    for nome in bande:
        print("        %-11s %s" % (nome, "  ".join(
            "eps=%s: %.4g" % (k, v) for k, v in sorted(bande[nome].items()))))

    # ================================================================ M il gap
    gap = {}
    for nome, geo in SCENE:
        per_eps = {}
        for eps in N2.EPS_SCANSIONE:
            om, _ = C2.quasi_energie(sc, geo, r, 1.0, eps)
            gmx, med = C2.gap_massimo(om)
            per_eps["%g" % eps] = {"gap": gmx, "spaziatura": med, "rapporto": gmx / med}
        gap[nome] = per_eps
    out["letture"]["M_gap"] = gap
    print("  M   gap massimo / spaziatura media:")
    for nome in gap:
        print("        %-11s %s" % (nome, "  ".join(
            "eps=%s: %.2f" % (k, v["rapporto"]) for k, v in sorted(gap[nome].items()))))

    # ================================================================ 3, 4, 5
    out["letture"]["3_conservata"] = {}
    out["letture"]["4_cluster"] = {}
    out["letture"]["5_materia_antimateria"] = {}
    varianti = [("lineare", None, 0.0)]
    for g in (0.5, 1.0, 2.0):
        for et, f, _n in N2.LE_DUE_V2:
            varianti.append(("(%s) g=%g" % (et, g), f, g))
    for nome, geo in (("identita", ident), ("curva", curva)):
        for et, f, g in varianti:
            chiave = "%s %s" % (nome, et)
            per_seme = [profilo2(sc, geo, r, 1.0, EPS_RIF, s, g, f, PASSI_LUNGHI)
                        for s in SEMI]
            cons = {}
            for cn, _fn in CANDIDATE:
                ris = [PASSI_LUNGHI * nest * EPS
                       * (float(np.max(np.abs(p["serie"][cn]))) or 1.0)
                       for p in per_seme]
                cl = [L1.classifica(p["tempo"], p["serie"][cn], ris[i])
                      for i, p in enumerate(per_seme)]
                e = [c["esito"] for c in cl]
                cons[cn] = {"esiti": e, "accordo": len(set(e)) == 1}
            out["letture"]["3_conservata"][chiave] = cons
            d_in = [p["dispersione"][0] for p in per_seme]
            d_fi = [p["dispersione"][-1] for p in per_seme]
            i_fi = [p["intrappolata"][-1] for p in per_seme]
            out["letture"]["4_cluster"][chiave] = {
                "media_iniziale": float(np.mean(d_in)),
                "media_finale": float(np.mean(d_fi)),
                "crescita": float(np.mean(d_fi) - np.mean(d_in)),
                "intrappolata": float(np.mean(i_fi))}
            out["letture"]["5_materia_antimateria"][chiave] = materia2(
                sc, geo, r, EPS_RIF, g, f)
        print("  4   %-11s %s" % (nome, "  ".join(
            "%s:%+.3f" % (k.split()[-1], v["crescita"])
            for k, v in out["letture"]["4_cluster"].items() if k.startswith(nome))))

    # ================================================================ O olonomia
    olo = {}
    for nome, geo in SCENE:
        prima = GE.olonomie(sc, geo["U"])
        C2.corri2(psi, sc, geo, r, 1.0, EPS_RIF, PASSI_CORTI)
        dopo = GE.olonomie(sc, geo["U"])
        olo[nome] = max(abs(a[1] - b[1]) + abs(a[2] - b[2])
                        for a, b in zip(prima, dopo))
    out["letture"]["O_olonomia"] = olo
    print("  O   olonomie, prima contro dopo: %s"
          % "  ".join("%s %.3g" % (k, v) for k, v in olo.items()))

    dati = (json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True)
            + NLN).encode("utf-8")
    io.open(os.path.join(USCITE, "letture_v2.json"), "wb").write(dati)
    print("  " + "-" * 96)
    print("  scritto proto_camminata/uscite/letture_v2.json")
    print("=" * 100)
    return 0


def materia2(sc, geo, r, eps, g, f):
    """### Il cluster e il suo **coniugato `C`**, nella scena **coniugata** se serve.

    ### ⭐ **E- QUI che il `v2` dice una cosa che il `v1` non poteva dire:** le componenti
    ### **si mescolano davvero**, quindi la simmetria **non passa per costruzione.**
    """
    fuori = {}
    det = np.linalg.det(geo["U"]).reshape(-1, 1, 1)
    geo_c = dict(geo)
    geo_c["U"] = geo["U"] / det
    for seme in SEMI[:2]:
        p, dentro = cluster2(sc, seme, 0)
        q = C2.coniuga2(p)
        fp, _ = C2.corri2(p, sc, geo, r, 1.0, eps, PASSI_LUNGHI, g, f)
        fq, _ = C2.corri2(q, sc, geo_c, r, 1.0, eps, PASSI_LUNGHI, g, f)
        dif = float(np.max(np.abs(C2.coniuga2(fp) - fq)))
        ip = L1.intrappolata(sc, fp, dentro)
        iq = L1.intrappolata(sc, fq, dentro)
        fuori[str(seme)] = {"coniugazione": dif, "intrappolata_piu": ip,
                            "intrappolata_meno": iq,
                            "asimmetria": abs(ip - iq) / (ip + iq) if (ip + iq) else -1.0}
    return fuori


if __name__ == "__main__":
    sys.exit(main())
