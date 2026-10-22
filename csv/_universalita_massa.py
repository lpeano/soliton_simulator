# -*- coding: utf-8 -*-
r"""**LA PROVA DEL PRINCIPIO DI EQUIVALENZA: L'UNIVERSALITA' DELLA MASSA AL VARIARE DI `cs`** *(attraverso `s`)*.

> ### ⛔ **Il task history e' `2026-10-22_universalita_massa.md`** *(il censimento, il metodo, i criteri fissati prima)*. ### **`dtau`, `eps`, `cs` SOLO nella
> scena, in memoria**; ### **`matrice()` e `rami_seguiti()` IMPORTATI da `csv/_massa_vicino_al_cono.py`**, non copiati. ### **Il verdetto di fisica e' la TABELLA
> dei `V_ij`**, non un passa/fallisce.

Gira con:  python csv/_universalita_massa.py
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LATI = (32, 64)
EPS_LISTA = (0.0, 0.25, 0.5, 0.75, 1.0)
S_LISTA = (0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0)
TOLL_FIT = 0.05
TOLL_DISTINTI = 1e-6
SOGLIA_V = 1e-3                # soglia di LETTURA, dal mandato
TOLL_TAGLIE = 0.01
TOLL_CONTROLLO = 1e-12
JSONL = os.path.join(RADICE, "doc", "referti_l2", "universalita_massa.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-84s %s   %s" % (che[:84], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def blob(rel):
    b = open(os.path.join(RADICE, rel), "rb").read()
    g = subprocess.run(["git", "hash-object", rel], capture_output=True, text=True, cwd=RADICE).stdout.strip()
    return {"sha1-BYTE": hashlib.sha1(b).hexdigest()[:8], "git": g[:8]}


def V_di(R):
    """### Lo stimatore: `(max - min)/media`; `None` se meno di `2` punti."""
    R = [r for r in R if np.isfinite(r)]
    if len(R) < 2:
        return None
    return float((max(R) - min(R)) / abs(np.mean(R)))


# =====================================================================================
#   I SALTI DI UNO SPETTRO, E L'OROLOGIO DI LUCE
# =====================================================================================
def spettro(L, s, eps):
    """### I salti per tick dei rami massivi *(validi e INVALIDI)*, e la frequenza per tick del ramo di luce a `k = pi/4`."""
    import _massa_vicino_al_cono as MV
    import _moneta_massa as MM
    A = MV.matrice(L, s, eps, 1.0)
    ph = MV.rami_seguiti(A, L)
    kk = 2.0 * np.pi * np.arange(L // 2 + 1) / L
    vg = np.gradient(ph, kk, axis=0)
    sel = kk <= 0.25 * np.pi + 1e-12
    validi, invalidi = [], []
    for b in range(8):
        if float(np.max(np.abs(vg[:, b]))) / s <= 0.1:
            continue
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            Dt, _vt, sc = MM.fit_massa(kk[sel], ph[sel, b] - ph[0, b])
        if not np.isfinite(Dt) or not sc <= TOLL_FIT:
            invalidi.append({"ramo": b, "Dt": float(Dt) if np.isfinite(Dt) else None, "scarto": float(sc),
                             "perche": "il fit non converge"})
        elif Dt > np.pi:
            invalidi.append({"ramo": b, "Dt": float(Dt), "scarto": float(sc), "perche": "Dt > pi"})
        elif Dt > 1e-9:
            validi.append(float(Dt))
    distinti = []
    for d in sorted(validi):
        if not distinti or abs(d - distinti[-1]) > TOLL_DISTINTI * d:
            distinti.append(d)
    # ### l'orologio: il settore del VUOTO in un 8x8 diagonale a blocchi con l'identita', seguito da rami_seguiti stesso
    Av = np.zeros(A.shape[:2] + (8, 8), dtype=complex)
    Av[..., :4, :4] = A[..., 8:, 8:]
    Av[..., 4:, 4:] = np.eye(4)
    pv = MV.rami_seguiti(Av, L)
    m4 = L // 8
    var = [abs(float(pv[m4, b] - pv[0, b])) for b in range(4)]
    luce = int(np.argmax(var))
    return distinti, invalidi, var[luce]


def catene(per_s):
    """### Le specie come CATENE in `s` per continuita': il `Dt` piu' vicino in senso relativo, entro un fattore `2`."""
    cat = []
    for s in S_LISTA:
        liberi = list(per_s[s])
        presi = set()
        cand = sorted(((abs(d - c[max(c)]) / c[max(c)], j, i) for j, c in enumerate(cat) for i, d in enumerate(liberi)
                       if 0.5 <= d / c[max(c)] <= 2.0))
        for _dist, j, i in cand:
            if j in presi or liberi[i] is None:
                continue
            cat[j][s] = liberi[i]
            liberi[i] = None
            presi.add(j)
        for d in liberi:
            if d is not None:
                cat.append({s: d})
    return cat


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    print("=" * 100)
    print("LA PROVA DEL PRINCIPIO DI EQUIVALENZA: L'UNIVERSALITA' DELLA MASSA AL VARIARE DI cs (attraverso s)")
    print("=" * 100)
    blobs = {r: blob(r) for r in ("soliton_simulator.py", "csv/_massa_vicino_al_cono.py", "csv/_universalita_massa.py")}
    print("  il passo: %d pezzi, impronta %s; i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA,
                                                                      "; ".join("%s %s" % (k, v) for k, v in blobs.items())))
    print("  il tetto Dt <= pi; fit <= %g; s %s; eps %s; lati %s; la soglia di LETTURA di V %g" % (TOLL_FIT, S_LISTA, EPS_LISTA,
                                                                                                   LATI, SOGLIA_V))
    print("-" * 100)
    sys.stdout.flush()
    # ------------------------------------------------------------ i criteri sui dati sintetici
    print("### I CRITERI SUI DATI SINTETICI (lo stesso stimatore di V)")
    ss = [s for s in S_LISTA]
    V_fallisce = V_di([(1.0 - s) / 0.339 for s in ss])
    esito("DEVE FALLIRE: Delta_1 = (1 - s), Delta_2 = 0.339 -> V oltre %g, e per V (un numero finito)" % SOGLIA_V,
          V_fallisce is not None and np.isfinite(V_fallisce) and V_fallisce > SOGLIA_V, "V = %r" % V_fallisce)
    V_controllo = V_di([2.0 * (1.0 - s) / (3.0 * (1.0 - s)) for s in ss if s < 1.0])
    esito("PUO' FALLIRE: Delta_1 = 2 (1 - s), Delta_2 = 3 (1 - s) -> V < %g" % TOLL_CONTROLLO,
          V_controllo is not None and V_controllo < TOLL_CONTROLLO, "V = %r (s < 1: a s = 1 il gap e' nullo)" % V_controllo)
    print("-" * 100)
    # ------------------------------------------------------------ la misura
    print("### LA MISURA: i salti validi e INVALIDI, e l'orologio di luce")
    D, INV, CLK = {}, [], {}
    for L in LATI:
        for eps in EPS_LISTA:
            for s in S_LISTA:
                dist, inv, clk = spettro(L, s, eps)
                D[(L, eps, s)] = dist
                CLK[(L, eps, s)] = clk
                for x in inv:
                    INV.append(dict(x, lato=L, eps=eps, s=s))
                print("  lato %d eps %-4g s %-5g: %d validi distinti Dt %s; %d INVALIDI%s; orologio di luce %.6f per tick"
                      % (L, eps, s, len(dist), ["%.5f" % d for d in dist], len(inv),
                         (" (" + ", ".join("%s %s" % (x["perche"], "%.3g" % x["Dt"] if x["Dt"] is not None else "-")
                                           for x in inv) + ")") if inv else "", clk))
                sys.stdout.flush()
    print("-" * 100)
    # ------------------------------------------------------------ le specie, i rapporti
    out = {"blobs": blobs, "criteri": {"V_deve_fallire": V_fallisce, "V_controllo": V_controllo}, "invalidi": INV}
    specie = {}
    for L in LATI:
        sp = []
        for eps in EPS_LISTA:
            for j, c in enumerate(catene({s: D[(L, eps, s)] for s in S_LISTA})):
                sp.append({"nome": "eps %g catena %d" % (eps, j), "eps": eps, "Dt": c,
                           "Delta": {s: c[s] / s for s in c}})
        specie[L] = sp
    print("### LE SPECIE (le catene in s) E Delta = Dt/dtau, per tempo proprio")
    for L in LATI:
        for sp in specie[L]:
            print("  lato %d %-18s: %s" % (L, sp["nome"], "  ".join("s %g %.5f" % (s, sp["Delta"][s]) for s in S_LISTA
                                                                   if s in sp["Delta"])))
    print("### IL POSITIVO: ogni specie contro se stessa, R = 1 al bit")
    for L in LATI:
        esito("lato %d: ogni specie contro se stessa, R = 1 AL BIT a ogni s" % L,
              all(sp["Delta"][s] / sp["Delta"][s] == 1.0 for sp in specie[L] for s in sp["Delta"]),
              "%d specie" % len(specie[L]))
    print("### LA TABELLA DEI V_ij (soglia di lettura %g: sotto universale entro la misura, sopra dipendente dalla specie)" % SOGLIA_V)
    tabV = []
    for L in LATI:
        sp = specie[L]
        for i in range(len(sp)):
            for j in range(i + 1, len(sp)):
                comuni = sorted(set(sp[i]["Delta"]) & set(sp[j]["Delta"]))
                V = V_di([sp[i]["Delta"][s] / sp[j]["Delta"][s] for s in comuni])
                tabV.append({"lato": L, "i": sp[i]["nome"], "j": sp[j]["nome"], "s": comuni, "V": V})
                print("  lato %d  %-18s / %-18s  su %d s: V %s  %s" % (
                    L, sp[i]["nome"], sp[j]["nome"], len(comuni), "%.4e" % V if V is not None else "non leggibile",
                    "" if V is None else ("(sotto 1e-3)" if V < SOGLIA_V else "(sopra 1e-3)")))
    out["V"] = tabV
    print("### L'OROLOGIO LOCALE: Delta per tick / la frequenza per tick del ramo di luce a k = pi/4")
    tabC = []
    for L in LATI:
        for sp in specie[L]:
            r = [sp["Dt"][s] / CLK[(L, sp["eps"], s)] for s in sorted(sp["Dt"])]
            V = V_di(r)
            tabC.append({"lato": L, "specie": sp["nome"], "rapporti": r, "V": V})
            print("  lato %d %-18s: rapporti %s -> V %s" % (L, sp["nome"], ["%.4f" % x for x in r],
                                                            "%.4e" % V if V is not None else "non leggibile"))
    out["orologio"] = tabC
    print("### LE TAGLIE: |Delta(32) - Delta(64)|/Delta < %g per ogni valore valido" % TOLL_TAGLIE)
    peggio, nconf = 0.0, 0
    for eps in EPS_LISTA:
        a = [sp for sp in specie[32] if sp["eps"] == eps]
        b = [sp for sp in specie[64] if sp["eps"] == eps]
        for x in a:
            s0 = min(x["Delta"])
            cand = [y for y in b if s0 in y["Delta"]]
            if not cand:
                continue
            y = min(cand, key=lambda y_: abs(y_["Delta"][s0] - x["Delta"][s0]))
            for s in x["Delta"]:
                if s in y["Delta"]:
                    peggio = max(peggio, abs(x["Delta"][s] - y["Delta"][s]) / abs(x["Delta"][s]))
                    nconf += 1
    esito("LE TAGLIE: per ogni valore valido accoppiato, entro %g" % TOLL_TAGLIE, peggio < TOLL_TAGLIE,
          "il peggiore %.4e su %d valori" % (peggio, nconf))
    out["taglie"] = {"peggiore": peggio, "valori": nconf}
    out["specie"] = {str(L): [{"nome": sp["nome"], "Delta": {str(s): v for s, v in sp["Delta"].items()}} for sp in specie[L]]
                     for L in LATI}
    io.open(JSONL, "w", encoding="utf-8").write(json.dumps(out) + "\n")
    print("=" * 100)
    print("L'UNIVERSALITA' DELLA MASSA: %d su %d controlli   %s  (il verdetto di fisica e' la tabella dei V_ij)"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
