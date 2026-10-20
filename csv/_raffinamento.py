# -*- coding: utf-8 -*-
r"""**LA PROVA DI RAFFINAMENTO SULL'INSTABILITA' DELLA MATERIA UNIFORME** — *una misura, nessun
codice di fisica.*

> ### ⛔ **Il task history e' `2026-10-20_raffinamento.md`** *(`e3c2bebf`)*, coi criteri fissati
> prima. Decisione di Luca del `2026-10-20`, `11:05`-`11:26`: ### **i risultati fisici sono
> quelli che CONVERGONO raffinando il campionamento.** ### **`LINEARE`, `Lambda_c` e le letture
> «alla Jeans» o di modulazione FERMI.**

## ⭐ TRE RISOLUZIONI *(`TAGLIA-FINITA`)*, LA REGOLA DI SCALA DI LUCA

lati `31`, `62`, `124` a `dtau` `0.125`, `0.0625`, `0.03125`: ### **valori per nodo invariati,
`dtau` proporzionale al passo della griglia**, stessa regione fisica *(`lato * a = 31`)*.
`R1` `x 0.1` `cs` acceso, rapporto `1`; `R2` `x 0.1` `cs` spento. ### **Il braccio `0`: a `31`
la serie di `9018188b` AL BIT.**

## ⭐ LE DUE PREVISIONI

`F` fisica: `lambda` in archi `x2` e `x4`; `A` artefatto: `x1` e `x1`. ### **Il verdetto dalla
media geometrica, a entrambe le risoluzioni; nessun test con tre punti.**

## ⚠ LA MEMORIA

A `124` i campi di tutti i tick sarebbero GB: ### **si tengono solo i campi che il fit usa**
*(al tick `T0`, al primo tick oltre l'`1%`, e l'ultimo)* -- ### **gli stessi che `29b997da`
leggeva dalla serie intera.**

Gira con:  python csv/_raffinamento.py
"""
import io
import json
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

import _instabilita_vuoto as IV                                 # noqa: E402
import _jeans_del_modello as JM                                 # noqa: E402

EPS = float(np.finfo(float).eps)
X = 0.1
RAPPORTO = 1.0
TEMPO = 1000.0                 # il tempo fisico di 9018188b
ARRESTO = 0.10                 # max|delta rho| / rho_m, come 9018188b
BUDGET_S = 4 * 3600.0          # dichiarato nel task history
LATO0 = 31
RISOLUZIONI = ((31, 0.125), (62, 0.0625), (124, 0.03125))
JSONL = os.path.join(RADICE, "doc", "referti_l2", "raffinamento.jsonl")
JSONL_9018 = os.path.join(RADICE, "doc", "referti_l2", "instabilita_dtau_piccolo.jsonl")
ZERO = {"R1": "I1 x 0.1 dtau 0.125", "R2": "I2 dtau 0.125"}
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-66s %s   %s" % (che[:66], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scena(lato, dtau):
    import scena_l2 as SC
    import statica_protocollo as PR
    lati = (lato, lato)
    inc, mot, st, par, _c, _p = SC.scena(dtau, PR.VUOTO, 0.0, PR.RAGGIO, False, True, False,
                                         PR.SEME, 1, lati=lati)
    st["psi_h"][...] = float(np.sqrt(X)) * PR.chi_allineato(lati, inc.m)
    return inc, mot, st, par


def braccio(nome, lato, dtau):
    import energia_pesata as EP
    import flussi_parziali as FP
    import tick as TK
    acceso = nome == "R1"
    inc, mot, st, par = scena(lato, dtau)
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    lc = RAPPORTO * lm
    tick = int(round(TEMPO / dtau))
    a = LATO0 / float(lato)
    fuori = {"nome": nome, "lato": lato, "dtau": dtau, "a": a, "tick_max": tick,
             "lambda_m": lm, "rho_m": rm, "lambda_c": lc,
             "cs_m": lm / (lm + lc) if acceso else 1.0, "fine": "tempo"}
    if acceso:
        FP.accendi_cs(mot, lc, st)
    soglia = IV.SOGLIA_PICCOLA * rm
    mr, ml, G = [], [], []
    campi = {}
    r0 = mot.densita_materia(st).copy()
    l0 = mot.densita_vuoto(st).copy()

    def foto(t):
        r = mot.densita_materia(st)
        l_ = mot.densita_vuoto(st)
        mr.append(float(np.max(np.abs(r - rm))))
        ml.append(float(np.max(np.abs(l_ - lm))))
        G.append(float(EP.g_dello_stato(mot, st, par)))
        if t == 1:
            campi["uno"] = (r.copy(), l_.copy())
        if t == IV.T0:
            campi["T0"] = (r.copy(), l_.copy())
        if t >= IV.T0 and "rho_1" not in campi and mr[-1] >= soglia:
            campi["rho_1"] = (t, r.copy())
        if t >= IV.T0 and "lam_1" not in campi and ml[-1] >= IV.SOGLIA_PICCOLA * lm:
            campi["lam_1"] = (t, l_.copy())
        campi["ultimo"] = (t, r.copy(), l_.copy())
    foto(0)
    fuori["non_converge"] = None
    t_inizio = time.time()
    try:
        for t in range(1, tick + 1):
            if acceso:
                TK.tick_con_cs(st, mot, par, lc, ())
            else:
                TK.tick(st, mot, par)
            foto(t)
            if mr[-1] > ARRESTO * rm:
                fuori["fine"] = "arresto 10%"
                break
            if time.time() - t_inizio > BUDGET_S:
                fuori["fine"] = "BUDGET superato al tick %d" % t
                break
    except AssertionError as e:
        fuori["non_converge"] = {"tick": len(mr), "msg": str(e)[:120]}
        fuori["fine"] = "non converge"
    fuori["secondi"] = time.time() - t_inizio
    fuori["tick_fatti"] = len(mr) - 1
    if "uno" in campi:
        fuori["m1_rho_ulp"] = float(np.max(np.abs(campi["uno"][0] - r0))) / (EPS * rm)
        fuori["m1_lam_ulp"] = float(np.max(np.abs(campi["uno"][1] - l0))) / (EPS * lm)
    fuori["m_rho"], fuori["m_lam"], fuori["G"] = mr, ml, G
    lati = (lato, lato)
    for chiave, m, scala, centro, idx in (("rho", mr, rm, rm, 0), ("lam", ml, lm, lm, 1)):
        g, b, t0, t1 = IV.gamma_del_tratto(m, scala)
        r = {"gamma": g, "barra": b, "T0": t0, "T1": t1,
             "zeri": int(np.sum(np.asarray(m)[t0:t1] == 0.0))}
        prima = campi.get(chiave + "_1")
        if prima is not None and prima[0] == t1:
            tc, campo = prima
        else:
            tc, campo = campi["ultimo"][0], campi["ultimo"][1 + idx]
        w = IV.onda(campo - centro, lati)
        r["onda"] = {"tick": tc, "lambda_archi": w[0], "lambda_fisico": w[0] * a,
                     "kx": w[1], "ky": w[2], "kx_pi": 2.0 * w[1] / lato,
                     "ky_pi": 2.0 * w[2] / lato, "frazione": w[3]}
        if g is not None and not r["zeri"] and "T0" in campi:
            gk = JM.gamma_k(campi["T0"][idx] - centro, campo - centro, t0, tc, lati)
            r["gamma_k"] = gk
        fuori[chiave] = r
    return fuori


def d_9018():
    fuori = {}
    with io.open(JSONL_9018, encoding="utf-8") as f:
        for riga in f:
            b = json.loads(riga)
            fuori[b["nome"]] = b
    return fuori


def stampa(b, ts):
    print("  %-3s lato %-4d dtau %-8g a %-5g tick %d/%d  [%s, %.0f s]%s"
          % (b["nome"], b["lato"], b["dtau"], b["a"], b["tick_fatti"], b["tick_max"],
             b["fine"], b["secondi"],
             "" if not b["non_converge"] else "   ### NON CONVERGE: il braccio si chiude li'"))
    for che in ("rho", "lam"):
        r = b[che]
        o = r["onda"]
        modo = ("modo (%d,%d) = (%.3f, %.3f) pi; lambda %.2f archi, %.3f fisico"
                % (o["kx"], o["ky"], o["kx_pi"], o["ky_pi"], o["lambda_archi"],
                   o["lambda_fisico"]))
        if r["gamma"] is None or r["zeri"]:
            print("      %-4s %s   %s" % (che, "zero esatto: NON cresce" if r["zeri"] else
                                          "tratto troppo corto", modo))
            continue
        s = b["dtau"] * b["cs_m"]
        instab = r["gamma"] >= ts * r["barra"]
        print("      %-4s gamma %+.4e +- %.1e (%6.1f barre) per tick, %+.4e tempo fisico  %-9s %s"
              % (che, r["gamma"], r["barra"], r["gamma"] / r["barra"], r["gamma"] / s,
                 "INSTABILE" if instab else "no", modo))
        if r.get("gamma_k"):
            sopra = [(q, l_) for q, l_, med, bar, _n in r["gamma_k"] if med >= ts * bar]
            if len(sopra) == len(r["gamma_k"]):
                lm_ = "NESSUNA lunghezza minima (crescono tutti gli anelli)"
            elif sopra:
                c = min(l_ for _q, l_ in sopra)
                lm_ = "la lunghezza minima: %.2f archi, %.3f fisico" % (c, c * b["a"])
            else:
                lm_ = "nessun anello sopra la soglia"
            print("           anelli sopra la soglia %d su %d; %s"
                  % (len(sopra), len(r["gamma_k"]), lm_))
    sys.stdout.flush()


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    import statica_protocollo as PR
    ts = JM.t_soglia()
    print("=" * 100)
    print("LA PROVA DI RAFFINAMENTO SULL'INSTABILITA' DELLA MATERIA UNIFORME -- una misura")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la materia uniforme: x %g, VUOTO %.1f, rapporto %g, SOLO rumore d'arrotondamento;"
          " R1 cs acceso, R2 cs spento" % (X, PR.VUOTO, RAPPORTO))
    print("  le risoluzioni (lato, dtau): %s; a = %d / lato; tempo fisico %g; arresto a"
          " max|drho| > %g rho_m; budget %.0f s per braccio"
          % (RISOLUZIONI, LATO0, TEMPO, ARRESTO, BUDGET_S))
    print("  il passo: %d pezzi, impronta %s; la soglia di Student %.3f barre (4 gradi);"
          " il verdetto F/A dalle previsioni, NESSUN test con tre punti"
          % (len(CM.ORDINE), CM.IMPRONTA, ts))
    print("  ### dichiarato prima: 31 e' DISPARI, 62 e 124 PARI -- k = pi esiste esattamente"
          " solo sui lati pari")
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    ieri = d_9018()
    bb = {}
    for lato, dtau in RISOLUZIONI:
        for nome in ("R1", "R2"):
            b = braccio(nome, lato, dtau)
            bb[(nome, lato)] = b
            with io.open(JSONL, "a", encoding="utf-8") as f:
                f.write(json.dumps(b) + "\n")
            ok = True
            if "m1_rho_ulp" in b:
                ok &= esito("M1 %s lato %d: il primo tick entro 256 ulp" % (nome, lato),
                            max(b["m1_rho_ulp"], b["m1_lam_ulp"]) <= JM.ULP_BANDA,
                            "rho %.1f, Lambda %.1f ulp" % (b["m1_rho_ulp"], b["m1_lam_ulp"]))
            if lato == LATO0:
                rif = ieri[ZERO[nome]]
                n = len(b["m_rho"])
                ok &= esito("braccio 0: %s a 31 = %s di 9018188b AL BIT (%d tick)"
                            % (nome, ZERO[nome], n - 1),
                            b["m_rho"] == rif["m_rho"][:n] and b["G"] == rif["G"][:n])
            stampa(b, ts)
            if not ok:
                print("### STOP: una prova e' caduta")
                return 1
            if b["fine"].startswith("BUDGET"):
                print("### STOP: il budget e' superato -- si riporta e ci si ferma, senza"
                      " ridurre la prova")
                return 1
    print("-" * 100)
    print("### IL VERDETTO, dalle previsioni (F: rapporti 2 e 4; A: 1 e 1; soglie 1.41 e 2)")
    for nome in ("R1", "R2"):
        for che in ("rho", "lam"):
            l0 = bb[(nome, 31)][che]["onda"]["lambda_archi"]
            r62 = bb[(nome, 62)][che]["onda"]["lambda_archi"] / l0
            r124 = bb[(nome, 124)][che]["onda"]["lambda_archi"] / l0
            if r62 > np.sqrt(2.0) and r124 > 2.0:
                v = "F (fisica)"
            elif r62 < np.sqrt(2.0) and r124 < 2.0:
                v = "A (artefatto)"
            else:
                v = "MISTO"
            gg = []
            for lato in (31, 62, 124):
                b = bb[(nome, lato)]
                g = b[che]["gamma"]
                gg.append(g / (b["dtau"] * b["cs_m"]) if g is not None else float("nan"))
            print("  %-3s %-4s lambda in archi 31: %.2f   62/31: %.3f   124/31: %.3f  -> %-14s"
                  "  gamma fisico %.4e %.4e %.4e (rapporti %.3f %.3f)"
                  % (nome, che, l0, r62, r124, v, gg[0], gg[1], gg[2], gg[1] / gg[0],
                     gg[2] / gg[0]))
    print("=" * 100)
    print("### %d/%d prove passate. NESSUNA LETTURA OLTRE IL VERDETTO F/A. LINEARE e Lambda_c"
          " FERMI." % tuple(OK))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
