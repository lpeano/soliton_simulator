# -*- coding: utf-8 -*-
"""LO SPETTRO — **gli stati INTRAPPOLATI sui cicli, e il gap DOVE LE BANDE SI INCONTRANO.**

> ## ⛔ **LA LETTURA `M` DEL `v2` MISURAVA LA COSA SBAGLIATA, e l'analisi del guardiano lo
> ## dice:** misurava il **gap MASSIMO ovunque sul cerchio** delle quasi-energie, non il gap
> ## **dove le bande si incontrano** — e il **`64.9`** a `eps = 0` veniva dalle **bande
> ## PIATTE** della camminata di Grover, cioe' **dagli stati intrappolati sui cicli.**

### ⭐ **CHE COSA SI MISURA ADESSO, e sono due cose diverse:**

| | la misura | perche' |
|---|---|---|
| `1` | **la molteplicita' di `+1` e `−1`** | sono **stati intrappolati sui cicli per pura interferenza**: non vanno da nessuna parte, e `~2` per ciclo |
| `2` | **il gap e la DENSITA' DI STATI vicino a `ω = 0` e `ω = π`** | e' **dove le bande si incontrano**, ed e' li' che **una massa aprirebbe un buco** |

### ⚠ **E LA MOLTEPLICITA' NON SI CONTA DAGLI AUTOVETTORI:** su un autospazio **degenere**
`eig` restituisce **una base qualunque**, e guardare se <<sono localizzati>> non vuol dire
niente. ### ✅ **Si contano gli AUTOVALORI** *(con il plateau sulla tolleranza)*, e si
**conferma col RANGO** di `U ∓ I` *(due metodi, non uno)*.

### ⭐ **IL RAPPORTO DI PARTECIPAZIONE** si usa **solo sugli stati NON degeneri**, ed e' il
numero di **nodi** su cui lo stato vive: `1/Σ_k p_k²` con `p_k` il peso del nodo `k`.

Gira con:  python proto_camminata/_spettro.py
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

import camminata2 as C2                                        # noqa: E402
import geometria as GE                                         # noqa: E402
import scena as SC                                             # noqa: E402

EPS = float(np.finfo(float).eps)
NL = chr(10)
USCITE = os.path.join(_QUI, "uscite")
SEME = 11
# ### ⛔ **LE TOLLERANZE DEL PLATEAU, DICHIARATE:** un conteggio che ### **non cambia
# ### su quattro decadi** non e- un artefatto della tolleranza. ### ⚠ **Se cambiasse,
# ### il numero non si potrebbe scrivere.**
TOLLERANZE = (1e-12, 1e-10, 1e-8, 1e-6)
EPS_SCANSIONE = (0.0, 0.25, 0.5, 1.0)


def conta_autovalori(lam, dove, tol):
    """Quanti autovalori stanno entro `tol` da `dove` *(sul piano complesso)*."""
    return int(np.sum(np.abs(lam - dove) < tol))


def rango_nullo(M, dove, tol):
    """### La molteplicita' **dal RANGO** di `U − dove·I`: ### **il secondo metodo.**

    ### ⭐ **E- indipendente da `eig`:** conta i **valori singolari** piccoli, che per una
    matrice unitaria **sono le distanze degli autovalori** da `dove`.
    """
    s = np.linalg.svd(M - dove * np.eye(M.shape[0]), compute_uv=False)
    return int(np.sum(s < tol))


def partecipazione(vec, sc):
    """### Su quanti **NODI** vive un autostato: `1/Σ p_k²`, con `p` il peso per nodo."""
    p = np.zeros(sc["n"], dtype=float)
    v = vec.reshape(-1, 2)
    np.add.at(p, sc["nodo"], np.sum(np.abs(v) ** 2, axis=1))
    s = float(np.sum(p))
    if s <= 0:
        return float("nan")
    p = p / s
    return 1.0 / float(np.sum(p ** 2))


def vicino_al_punto(om, dim, dove):
    """### Il **gap** dal punto d'incontro e la **densita' di stati** attorno.

    ### ⛔ **LE FINESTRE SONO DERIVATE, non scelte:** la spaziatura media di `dim`
    autovalori sul cerchio e' `2π/dim`, e le finestre sono **`k` spaziature** con
    `k = 1, 2, 4, 8`. ### ✅ **Cosi' <<quanti stati ci sono vicino>> e' confrontabile fra
    grafi di taglia diversa.**
    """
    d = np.abs(np.angle(np.exp(1j * (om - dove))))
    media = 2.0 * math.pi / dim
    fuori = {"gap": float(np.min(d)), "gap_in_spaziature": float(np.min(d) / media),
             "spaziatura_media": media, "finestre": {}}
    for k in (1, 2, 4, 8):
        fuori["finestre"]["%d" % k] = int(np.sum(d < k * media))
    return fuori


def analizza(sc, geo, r, eps, con_rango=False):
    """Tutto quello che si legge da uno spettro, per una scena e un `eps`."""
    M = C2.matrice_passo(sc, geo, r, 1.0, eps)
    dim = M.shape[0]
    lam, vec = np.linalg.eig(M)
    om = np.angle(lam)
    fuori = {"dim": dim, "unitaria": float(np.max(np.abs(
        M.conj().T @ M - np.eye(dim)))), "plateau": {}}
    for dove, nome in ((1.0, "piu_uno"), (-1.0, "meno_uno")):
        fuori["plateau"][nome] = {"%g" % t: conta_autovalori(lam, dove, t)
                                  for t in TOLLERANZE}
        fuori[nome] = conta_autovalori(lam, dove, TOLLERANZE[1])
        fuori[nome + "_stabile"] = (len(set(fuori["plateau"][nome].values())) == 1)
        if con_rango:
            fuori[nome + "_dal_rango"] = rango_nullo(M, dove, TOLLERANZE[1])
    fuori["zero"] = vicino_al_punto(om, dim, 0.0)
    fuori["pi"] = vicino_al_punto(om, dim, math.pi)
    # ### il rapporto di partecipazione, SOLO sugli stati NON degeneri
    lontani = [j for j in range(dim)
               if abs(abs(lam[j]) - 1.0) < 1e-9
               and min(abs(lam[j] - 1.0), abs(lam[j] + 1.0)) > 1e-6]
    pr = [partecipazione(vec[:, j], sc) for j in lontani[:200]]
    fuori["partecipazione_non_degeneri"] = {
        "quanti": len(lontani),
        "mediana": float(np.median(pr)) if pr else float("nan"),
        "minima": float(np.min(pr)) if pr else float("nan")}
    return fuori


def scala_di_taglia(taglie=(60, 120, 240)):
    """### IL GAP AL PUNTO D-INCONTRO, su TRE TAGLIE del grafo REGOLARE.

    ### ⛔ **E- cio- che rende difendibile un <<nessun gap>>:** un gap VERO e-
    ### **O(1) in quasi-energia**, quindi ### **cresce come `dim` se misurato in
    spaziature**; un gap che resta ### **O(1) in spaziature** ### **non e- un gap**, e-
    solo la spaziatura media.
    ### ⚠ **E due taglie sono una retta per due punti** *(`TAGLIA-FINITA`)*: qui ne servono TRE.
    """
    fuori = {}
    for n in taglie:
        sc = SC.regolare(n=n)
        uno = np.ones(sc["n"], dtype=float)
        geo = GE.scena_identita(sc)
        per_eps = {}
        for eps in (0.0, 1.0):
            M = C2.matrice_passo(sc, geo, uno, 1.0, eps)
            om = np.angle(np.linalg.eigvals(M))
            z = vicino_al_punto(om, M.shape[0], 0.0)
            per_eps["%g" % eps] = {"gap": z["gap"],
                                   "gap_in_spaziature": z["gap_in_spaziature"],
                                   "stati": M.shape[0]}
        fuori["%d" % n] = per_eps
        print("     n=%-4d stati=%-5d  gap(0) eps=0: %.3g (%.2f sp)   eps=1: %.3g "
              "(%.2f sp)"
              % (n, 4 * sc["m"], per_eps["0"]["gap"], per_eps["0"]["gap_in_spaziature"],
                 per_eps["1"]["gap"], per_eps["1"]["gap_in_spaziature"]))
    return fuori


def main():
    SC._niente_simulatore()
    os.makedirs(USCITE, exist_ok=True)
    out = {}
    print("=" * 100)
    print("LO SPETTRO: GLI STATI INTRAPPOLATI, E IL GAP DOVE LE BANDE SI INCONTRANO")
    print("=" * 100)
    for nome_g, sc in (("irregolare", SC.irregolare()), ("regolare", SC.regolare())):
        cicli = sc["m"] - sc["n"] + 1
        r = SC.ritmi(sc, SEME)
        uno = np.ones(sc["n"], dtype=float)
        print("  %s: n=%d archi=%d stati=%d   cicli indipendenti %d"
              % (nome_g, sc["n"], sc["m"], 4 * sc["m"], cicli))
        out[nome_g] = {"n": sc["n"], "archi": sc["m"], "stati": 4 * sc["m"],
                       "cicli": cicli, "scene": {}}
        for nome_s, geo in (("identita", GE.scena_identita(sc)),
                            ("curva", GE.scena_curva(sc, SEME))):
            out[nome_g]["scene"][nome_s] = {}
            for eps in EPS_SCANSIONE:
                a = analizza(sc, geo, uno, eps, con_rango=(eps == 0.0))
                out[nome_g]["scene"][nome_s]["%g" % eps] = a
                print("     %-9s eps=%-4g  +1: %4d  -1: %4d  (stabile %s/%s)   "
                      "gap(0): %6.2f sp   gap(pi): %6.2f sp   DOS(0,1sp): %d"
                      % (nome_s, eps, a["piu_uno"], a["meno_uno"],
                         "si" if a["piu_uno_stabile"] else "NO",
                         "si" if a["meno_uno_stabile"] else "NO",
                         a["zero"]["gap_in_spaziature"], a["pi"]["gap_in_spaziature"],
                         a["zero"]["finestre"]["1"]))
                if eps == 0.0:
                    print("        e dal RANGO di U-I e U+I: %d e %d   ### secondo metodo"
                          % (a["piu_uno_dal_rango"], a["meno_uno_dal_rango"]))
                    print("        intrappolati: %d su %d = %.1f%%   ### %.2f per ciclo"
                          % (a["piu_uno"] + a["meno_uno"], a["dim"],
                             100.0 * (a["piu_uno"] + a["meno_uno"]) / a["dim"],
                             (a["piu_uno"] + a["meno_uno"]) / float(cicli)))
    print("  LA SCALA DI TAGLIA, sul grafo REGOLARE (il gap al punto d-incontro):")
    out["scala_di_taglia"] = scala_di_taglia()
    dati = (json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True)
            + NL).encode("utf-8")
    io.open(os.path.join(USCITE, "spettro.json"), "wb").write(dati)
    print("  " + "-" * 96)
    print("  scritto proto_camminata/uscite/spettro.json")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
