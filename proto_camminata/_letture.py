# -*- coding: utf-8 -*-
"""LE SETTE LETTURE — **i numeri, e le soglie sono quelle del task history.**

> ### ⛔ **NIENTE SI DECIDE QUI:** criteri, previsioni e soglie stanno in
> `doc/TASK_HISTORY/2026-10-10_prototipo_camminata.md`, **committato prima del codice**.
> ### **Questo file MISURA**, e scrive `proto_camminata/uscite/letture.json`.

| | la lettura | che cosa misura |
|---|---|---|
| `1a` | **isotropia della camminata** | rinumerazione di nodi e archi, **nei due modi di somma** |
| `1b` | **anisotropia dell'INTEGRATORE a strati** | la differenza fra **due ordini di strati**, in funzione di `dt` |
| `2` | **cono** | oltre `T` archi, **zero esatto** |
| `3` | **quantita' conservata** | **quattro candidate dichiarate**, e la deriva di ognuna su `4` semi |
| `4` | **cluster** | dispersione delle frequenze, e **frazione intrappolata** |
| `5` | **materia / antimateria** | il cluster e il suo **coniugato `C`** |
| `6` | **`r=1`** | coincide col `dt` globale **al bit** |
| `7` | **il gauge, ROVESCIATO** | `c·r` **CAMBIA** la fisica, e di quanto |

### ⚠ **LA FREQUENZA DI UN NODO, come l'ho definita PRIMA di misurarla:** la fase si prende
**sull'ampiezza TOTALE del nodo** *(non estremita' per estremita')*, e la dispersione e'
**pesata con `ρ`** — cosi' **nessun pavimento e nessuna soglia a mano** *(`A11`)*.

Gira con:  python proto_camminata/_letture.py
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
import _presidio                                               # noqa: E402

_presidio.avvia(__file__)

import camminata as CM                                         # noqa: E402
import nonlineare as NL                                        # noqa: E402
import scena as SC                                             # noqa: E402

EPS = float(np.finfo(float).eps)
NLN = chr(10)
USCITE = os.path.join(_QUI, "uscite")

# ### ⛔ **I NUMERI DELLA SCENA, DICHIARATI NEL TASK HISTORY** -- e qui si rileggono,
# ### non si reinventano.
SEMI = (11, 23, 37, 53)
PASSI_LUNGHI = 400
PASSI_CORTI = 60
# ### ⚠ **I `dt` della lettura `1b`: POTENZE DI DUE**, cosi- il dimezzamento e-
# ### ### **esatto** e la pendenza non misura il mio arrotondamento.
DT_SCALA = (0.5, 0.25, 0.125, 0.0625)
# ### ⚠ **I fattori della lettura `7`: POTENZE DI DUE**, per la stessa ragione.
FATTORI = (0.5, 2.0)


def pendenza(x, y):
    """### `(pendenza, sigma)` ai minimi quadrati. ### **La soglia e' il SUO sigma.**"""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    if n < 3:
        return float("nan"), float("inf")
    sx, sy = x.mean(), y.mean()
    sxx = float(np.sum((x - sx) ** 2))
    if sxx == 0.0:
        return float("nan"), float("inf")
    b = float(np.sum((x - sx) * (y - sy)) / sxx)
    res = y - (sy + b * (x - sx))
    s2 = float(np.sum(res ** 2)) / (n - 2) if n > 2 else 0.0
    return b, math.sqrt(s2 / sxx) if sxx > 0 else float("inf")


def classifica(t, v, risoluzione=None):
    """### I TRE ESITI DISTINTI del mandato: ### **conservata · oscillante limitata ·
    deriva.**

    ### ✅ **E la soglia e' sempre <<entro `3 sigma` della PROPRIA stima>>:** niente
    numero scelto a mano. ### ⚠ **<<Oscillante limitata>> si decide su una SECONDA
    pendenza**, quella della ### **escursione corrente** -- se anche quella e' piatta,
    l-oscillazione ### **non cresce.**
    """
    v = np.asarray(v, dtype=float)
    scala = float(np.max(np.abs(v))) or 1.0
    # ### ⛔ **PRIMA LA RISOLUZIONE, POI LA STATISTICA -- e l-ordine non e- un
    # ### dettaglio:** trovato il 2026-10-10, al primo giro delle letture.
    # ### ⚠ **IL FALSO ROSSO:** la norma della camminata lineare varia
    # ### ### **solo per arrotondamento** *(`1.2e-15`, misurato dal collaudo)*, e un
    # ### test di pendenza su quei valori ### **trova SEMPRE una tendenza
    # ### significativa**, perche- ### **il suo sigma E- l-arrotondamento.**
    # ### ✅ **Quindi: se l-ESCURSIONE TOTALE sta sotto la risoluzione della misura,
    # ### la grandezza e- CONSERVATA e non si fitta niente.**
    # ### ⭐ **E la risoluzione NON e- scelta:** e- `passi * n_estremita * eps`, la
    # ### ### **stessa formula della soglia `S3`** del task history.
    esc_tot = float(np.max(v) - np.min(v))
    if risoluzione is not None and esc_tot <= risoluzione:
        return {"esito": "CONSERVATA", "pendenza": 0.0, "sigma": 0.0,
                "pendenza_escursione": 0.0, "sigma_escursione": 0.0, "scala": scala,
                "escursione": esc_tot, "risoluzione": risoluzione,
                "nota": "escursione SOTTO la risoluzione della misura: non c-e- niente da "
                        "fittare"}
    b, sb = pendenza(t, v / scala)
    # l-escursione su finestre crescenti: se cresce, non e- <<limitata>>
    fin = max(8, len(v) // 8)
    esc, tt = [], []
    for i in range(fin, len(v), fin):
        esc.append(float(np.max(v[:i]) - np.min(v[:i])) / scala)
        tt.append(t[i - 1])
    be, sbe = pendenza(tt, esc) if len(esc) >= 3 else (float("nan"), float("inf"))
    piatta = abs(b) <= 3.0 * sb
    esc_piatta = (not math.isnan(be)) and abs(be) <= 3.0 * sbe
    if piatta and esc_piatta:
        esito = "CONSERVATA"
    elif piatta:
        esito = "OSCILLANTE LIMITATA"
    else:
        esito = "DERIVA"
    return {"esito": esito, "pendenza": b, "sigma": sb, "pendenza_escursione": be,
            "sigma_escursione": sbe, "scala": scala, "escursione": esc_tot,
            "risoluzione": risoluzione}


# =====================================================================================
#   LE QUANTITA' CANDIDATE -- dichiarate, e ognuna con la sua forma
# =====================================================================================
def _cand_norma(psi, sc, r, dt, g, f):
    return CM.norma(psi)


def _cand_quasi(psi, sc, r, dt, g, f):
    """`Re<psi|U|psi>` con `U` il passo COMPLETO: per la lineare e' conservata."""
    return float(CM.quasi_energia(psi, sc, r, dt, g, f).real)


def _cand_energia_pari(psi, sc, r, dt, g, f):
    """`Re<psi|U_lin|psi> + (g/2) somma rho^2 dtau`: la forma naturale per `(A)`."""
    lin = float(CM.quasi_energia(psi, sc, r, dt).real)
    rho = CM.rho_nodo(psi, sc)
    return lin + 0.5 * g * float(np.sum(rho ** 2 * r * dt))


def _cand_energia_dispari(psi, sc, r, dt, g, f):
    """`Re<psi|U_lin|psi> + (g/2) somma s^2 dtau`: la forma naturale per `(B)`."""
    lin = float(CM.quasi_energia(psi, sc, r, dt).real)
    s = CM.s_nodo(psi, sc)
    return lin + 0.5 * g * float(np.sum(s ** 2 * r * dt))


CANDIDATE = (
    ("la norma", _cand_norma),
    ("la quasi-energia del passo", _cand_quasi),
    ("energia + termine PARI", _cand_energia_pari),
    ("energia + termine DISPARI", _cand_energia_dispari),
)


# =====================================================================================
#   IL CLUSTER -- costruito, e DICHIARATO
# =====================================================================================
def cluster(sc, seme, banda=0):
    """### Un cluster **in fase** nella banda scelta: un nodo e i suoi vicini a `1` arco.

    ### ⚠ **IN FASE vuol dire FASE UGUALE**, non <<ampiezza uguale>>: le ampiezze
    seguono il grado, perche' ### **un nodo con sei archi ha sei estremita'.**
    """
    rng = np.random.default_rng(seme)
    centro = int(rng.integers(0, sc["n"]))
    dentro = set([centro] + list(sc["vicini"][centro]))
    psi = CM.stato_zero(sc)
    nodo = sc["nodo"]
    for e in range(2 * sc["m"]):
        if int(nodo[e]) in dentro:
            psi[e, banda] = 1.0
    nn = math.sqrt(CM.norma(psi))
    return psi / nn, sorted(dentro)


def frequenze(sc, psi_a, psi_b):
    """### `omega_k` dall'ampiezza **TOTALE** del nodo, e il peso e' `rho`."""
    n = sc["n"]
    A = np.zeros((n, 2), dtype=complex)
    B = np.zeros((n, 2), dtype=complex)
    np.add.at(A, sc["nodo"], psi_a)
    np.add.at(B, sc["nodo"], psi_b)
    a = A.sum(axis=1)
    b = B.sum(axis=1)
    om = np.angle(b * np.conj(a))
    peso = np.abs(a) ** 2
    return om, peso


def dispersione(om, peso, dentro):
    """### La deviazione standard **pesata con `rho`**, dentro il cluster."""
    idx = np.asarray(dentro, dtype=int)
    w = peso[idx]
    tot = float(np.sum(w))
    if tot <= 0.0:
        return float("nan")
    o = om[idx]
    med = float(np.sum(w * o) / tot)
    return math.sqrt(float(np.sum(w * (o - med) ** 2) / tot))


def intrappolata(sc, psi, dentro):
    """### La frazione di `rho` **ancora dentro** i nodi iniziali del cluster."""
    rho = CM.rho_nodo(psi, sc)
    return float(np.sum(rho[np.asarray(dentro, dtype=int)]) / np.sum(rho))


def profilo(sc, r, dt, seme, g, f, passi, banda=0):
    """Una corsa: `(dispersione finale, frazione intrappolata, serie delle candidate)`."""
    psi, dentro = cluster(sc, seme, banda)
    serie = {nome: [] for nome, _fn in CANDIDATE}
    disp, intr, tempo = [], [], []
    prec = psi
    for t in range(1, passi + 1):
        nuovo = CM.passo(prec, sc, r, dt, g, f)
        if t % 4 == 0 or t == passi:
            om, peso = frequenze(sc, prec, nuovo)
            disp.append(dispersione(om, peso, dentro))
            intr.append(intrappolata(sc, nuovo, dentro))
            tempo.append(t)
            for nome, fn in CANDIDATE:
                serie[nome].append(fn(nuovo, sc, r, dt, g, f))
        prec = nuovo
    return {"tempo": tempo, "dispersione": disp, "intrappolata": intr,
            "serie": serie, "dentro": dentro, "fine": prec}


def main():
    SC._niente_simulatore()
    os.makedirs(USCITE, exist_ok=True)
    out = {"scena": {}, "letture": {}}
    sc = SC.irregolare()
    reg = SC.regolare()
    r = SC.ritmi(sc, SEMI[0])
    gmax = int(sc["grado"].max())
    out["scena"] = {"nome": sc["nome"], "n": sc["n"], "archi": sc["m"],
                    "estremita": 2 * sc["m"],
                    "gradi": sorted(set(sc["grado"].tolist())),
                    "regolare": reg["nome"], "semi": list(SEMI)}
    print("=" * 100)
    print("LE SETTE LETTURE DEL PROTOTIPO")
    print("=" * 100)
    print("  scena: %s   estremita-: %d   gradi: %s"
          % (sc["nome"], 2 * sc["m"], out["scena"]["gradi"]))

    # ================================================================ 1a
    psi = CM.stato_casuale(sc, SEMI[0])
    nuova, pn, mappa = SC.rinumera(sc, 23)
    rn = np.empty_like(r)
    rn[pn] = r
    uno = {}
    for esatta in (True, False):
        f1, _ = CM.corri(psi, sc, r, 1.0, PASSI_CORTI, esatta=esatta)
        pp = np.zeros_like(psi)
        pp[mappa] = psi
        f2, _ = CM.corri(pp, nuova, rn, 1.0, PASSI_CORTI, esatta=esatta)
        rip = np.zeros_like(f2)
        rip[mappa] = f1
        uno["fsum" if esatta else "numpy"] = float(np.max(np.abs(rip - f2)))
    uno["soglia"] = PASSI_CORTI * gmax * EPS * math.sqrt(CM.norma(psi))
    out["letture"]["1a_isotropia_camminata"] = uno
    print("  1a  isotropia: fsum %.3g   numpy %.3g   soglia %.3g"
          % (uno["fsum"], uno["numpy"], uno["soglia"]))

    # ================================================================ 1b
    out["letture"]["1b_anisotropia_integratore"] = anisotropia_integratore(sc)

    # ================================================================ 2
    d0 = SC.distanze(sc, 0)
    T = max(1, int(d0.max()) // 2)
    e0 = int(np.nonzero(sc["nodo"] == 0)[0][0])
    a = CM.stato_zero(sc)
    a[e0, 0] = 1.0
    b = a.copy()
    b[e0, 0] = 1.0 + 1e-3
    fa, _ = CM.corri(a, sc, r, 1.0, T)
    fb, _ = CM.corri(b, sc, r, 1.0, T)
    dif = np.abs(fa - fb).sum(axis=1)
    fuori = dif[d0[sc["nodo"]] > T]
    out["letture"]["2_cono"] = {"T": T, "eccentricita": int(d0.max()),
                                "estremita_fuori": int(fuori.size),
                                "max_fuori": float(np.max(fuori)) if fuori.size else -1.0,
                                "nodi_oltre": int(np.sum(d0 > T))}
    print("  2   cono: T=%d, max fuori %.3g su %d estremita-"
          % (T, out["letture"]["2_cono"]["max_fuori"], int(fuori.size)))

    # ================================================================ 3, 4, 5, 7
    out["letture"]["3_conservata"] = {}
    out["letture"]["4_cluster"] = {}
    out["letture"]["5_materia_antimateria"] = {}
    varianti = [("lineare", None, 0.0)]
    for g in NL.G_SCANSIONE:
        if g == 0.0:
            continue
        for nome, f, _nota in NL.LE_DUE:
            varianti.append(("(%s) g=%g" % (nome, g), f, g))

    for etichetta, f, g in varianti:
        per_seme = [profilo(sc, r, 1.0, s, g, f, PASSI_LUNGHI) for s in SEMI]
        # --- lettura 3: le quattro candidate, su ogni seme
        cons = {}
        for nome, _fn in CANDIDATE:
            # ### la risoluzione della misura, DALLA STESSA FORMULA di `S3`
            ris = [PASSI_LUNGHI * 2 * sc["m"] * EPS
                   * (float(np.max(np.abs(p["serie"][nome]))) or 1.0) for p in per_seme]
            cl = [classifica(p["tempo"], p["serie"][nome], ris[i])
                  for i, p in enumerate(per_seme)]
            esiti = [c["esito"] for c in cl]
            cons[nome] = {"esiti": esiti,
                          "accordo": len(set(esiti)) == 1,
                          "pendenze": [c["pendenza"] for c in cl],
                          "sigma": [c["sigma"] for c in cl]}
        out["letture"]["3_conservata"][etichetta] = cons
        # --- lettura 4: dispersione e intrappolamento
        d_in = [p["dispersione"][0] for p in per_seme]
        d_fi = [p["dispersione"][-1] for p in per_seme]
        i_fi = [p["intrappolata"][-1] for p in per_seme]
        out["letture"]["4_cluster"][etichetta] = {
            "dispersione_iniziale": [float(x) for x in d_in],
            "dispersione_finale": [float(x) for x in d_fi],
            "intrappolata_finale": [float(x) for x in i_fi],
            "media_iniziale": float(np.mean(d_in)),
            "media_finale": float(np.mean(d_fi)),
            "sigma_finale": float(np.std(d_fi, ddof=1)) if len(d_fi) > 1 else 0.0,
            "perde_coerenza": bool(np.mean(d_fi) > np.mean(d_in)
                                   + 3.0 * (np.std(d_fi, ddof=1) if len(d_fi) > 1 else 0.0)),
        }
        print("  4   %-14s disp %.4g -> %.4g   intrappolata %.3f"
              % (etichetta, np.mean(d_in), np.mean(d_fi), np.mean(i_fi)))
        # --- lettura 5: il cluster e il suo coniugato
        out["letture"]["5_materia_antimateria"][etichetta] = materia(sc, r, g, f)

    # ================================================================ 6
    uni = np.ones(sc["n"], dtype=float)
    f1, _ = CM.corri(psi, sc, uni, 1.0, PASSI_CORTI)
    f2 = psi.copy()
    for _ in range(PASSI_CORTI):
        f2 = CM.passo_dt_globale(f2, sc, 1.0)
    out["letture"]["6_r_uguale_uno"] = {"max_differenza": float(np.max(np.abs(f1 - f2)))}
    print("  6   r=1 contro dt globale: %.3g" % out["letture"]["6_r_uguale_uno"][
        "max_differenza"])

    # ================================================================ 7
    out["letture"]["7_gauge_rovesciato"] = gauge(sc, r, uno["soglia"])

    # ================================================================ si scrive
    dati = (json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True)
            + NLN).encode("utf-8")
    io.open(os.path.join(USCITE, "letture.json"), "wb").write(dati)
    print("  " + "-" * 96)
    print("  scritto proto_camminata/uscite/letture.json")
    print("=" * 100)
    return 0


def anisotropia_integratore(sc):
    """### **L'ANISOTROPIA DELL'INTEGRATORE A STRATI**, in funzione di `dt`.

    ### ⛔ **E- QUESTO il confronto che si puo- fare**, e l'annotazione del task history
    dice perche': *«camminata contro integratore»* ### **non tende a zero**, perche' sono
    ### **due dinamiche diverse**. ### ✅ **Qui si misura l'ARTEFATTO**: la differenza
    fra ### **DUE ORDINI DI STRATI** della stessa scena.
    """
    fuori = {"dt": list(DT_SCALA), "differenze": [], "pendenza": None, "sigma": None,
              "nota": ""}
    try:
        sys.path.insert(0, os.path.join(RADICE, "primo_ordine"))
        sys.path.insert(0, os.path.join(RADICE, "primo_ordine", "config"))
        sys.path.insert(0, os.path.join(RADICE, "primo_ordine", "leggi"))
        import hamiltoniana as HAM
        import passo as PA
        import schema_config as CFG
        import stato as ST
        C = CFG.carica(os.path.join(RADICE, "primo_ordine", "config", "prova.yaml"))
        T = [m for m in HAM.carica_termini() if m.LEGGE in C["leggi_attive"]]
        ii = np.array([a for a, _b in sc["archi"]], dtype=int)
        jj = np.array([b for _a, b in sc["archi"]], dtype=int)
        st = ST.nuovo(sc["n"])
        rng = np.random.default_rng(SEMI[0])
        st["psi"] = (rng.standard_normal((sc["n"], 2))
                     + 1j * rng.standard_normal((sc["n"], 2)))
        st["psi"] /= math.sqrt(float(np.sum(np.abs(st["psi"]) ** 2)))
        ss = PA.strati(ii, jj)
        for dt in DT_SCALA:
            u, _ = PA.passo_locale(st, ii, jj, dt, T, C["iterazioni"], C["toll"], ss)
            v, _ = PA.passo_locale(st, ii, jj, dt, T, C["iterazioni"], C["toll"],
                                   tuple(reversed(ss)))
            fuori["differenze"].append(float(np.max(np.abs(u["psi"] - v["psi"]))))
        lx = [math.log(x) for x in DT_SCALA]
        ly = [math.log(y) if y > 0 else -700.0 for y in fuori["differenze"]]
        b, sb = pendenza(lx, ly)
        fuori["pendenza"] = b
        fuori["sigma"] = sb
        fuori["strati"] = len(ss)
        print("  1b  anisotropia integratore: pendenza %.3f +/- %.3f su %d dt (%d strati)"
              % (b, sb, len(DT_SCALA), len(ss)))
    except Exception as e:                                     # noqa: BLE001
        fuori["nota"] = "NON MISURATA: %s: %s" % (type(e).__name__, e)
        print("  1b  anisotropia integratore: %s" % fuori["nota"])
    return fuori


def materia(sc, r, g, f):
    """### Il cluster nella banda `+` e il suo **coniugato `C`** nella banda `−`."""
    fuori = {}
    for seme in SEMI[:2]:
        p, dentro = cluster(sc, seme, 0)
        q = CM.coniuga(p)
        fp, _ = CM.corri(p, sc, r, 1.0, PASSI_LUNGHI, g, f)
        fq, _ = CM.corri(q, sc, r, 1.0, PASSI_LUNGHI, g, f)
        # ### ⭐ **SE `C` E- UNA SIMMETRIA, i due run sono CONIUGATI AL BIT.**
        dif = float(np.max(np.abs(CM.coniuga(fp) - fq)))
        ip = intrappolata(sc, fp, dentro)
        iq = intrappolata(sc, fq, dentro)
        asim = abs(ip - iq) / (ip + iq) if (ip + iq) > 0 else float("nan")
        fuori[str(seme)] = {"coniugazione_al_bit": dif, "intrappolata_piu": ip,
                            "intrappolata_meno": iq, "asimmetria": asim}
    return fuori


def gauge(sc, r, soglia):
    """### **LA LETTURA `7`, ROVESCIATA:** `c·r` **CAMBIA** la fisica, e di quanto."""
    fuori = {"soglia_arrotondamento": soglia, "fattori": {}}
    base = profilo(sc, r, 1.0, SEMI[0], 1.0, NL.fase_dispari, PASSI_CORTI)
    for c in FATTORI:
        alt = profilo(sc, c * r, 1.0, SEMI[0], 1.0, NL.fase_dispari, PASSI_CORTI)
        d_disp = abs(alt["dispersione"][-1] - base["dispersione"][-1])
        d_intr = abs(alt["intrappolata"][-1] - base["intrappolata"][-1])
        d_psi = float(np.max(np.abs(alt["fine"] - base["fine"])))
        fuori["fattori"]["%g" % c] = {
            "delta_dispersione": float(d_disp), "delta_intrappolata": float(d_intr),
            "delta_stato": d_psi,
            "oltre_arrotondamento": bool(d_psi > soglia)}
        print("  7   c=%g: delta stato %.3g, delta dispersione %.3g, delta intrappolata "
              "%.3g" % (c, d_psi, d_disp, d_intr))
    return fuori


if __name__ == "__main__":
    sys.exit(main())
