# -*- coding: utf-8 -*-
r"""**L'INSTABILITA' DELLA MATERIA UNIFORME, RIFATTA A `dtau 0.125`** — *una misura, nessun codice
di fisica.*

> ### ⛔ **Il task history e' `2026-10-20_instabilita_a_dtau_piccolo.md`** *(`fa90a49e`)*, coi
> criteri fissati prima. Decisione di Luca del `2026-10-20` alle `10:27`: ### **il verdetto
> della scala del salto e' `P2`**, e a `dtau 0.125` l'escursione di `H` sulla materia uniforme
> sta ### **sotto la banda `B`**. ### **`LINEARE`, `Lambda_c` e le letture «alla Jeans» FERMI.**

## ⭐ I BRACCI *(SOLO rumore d'arrotondamento, rapporto `1`; a `dtau 0.125` e `0.25`)*

`C2` la sola camminata, senza `CAMM-MATERIA-VUOTO`, `cs` spento, `x 0.1` · `I1` `cs` acceso,
`x` in `{0.01, 0.1, 1}` · `I2` `cs` spento, `x 0.1`. ### **Tempo totale `1000`**, arresto quando
`max|delta rho|` supera il `10%` di `rho_m`.

## ⛔ LE PROVE *(se una cade: STOP)*

`P0a` ### **`I1` a `x 0.1`, `dtau 0.25` riproduce `D3` di `29b997da` AL BIT** · `P0b` i termini
di `H` ricostruiti al bit a ogni tick · `M1` l'equilibrio al tick `0`.

## ⭐ LE MISURE

gamma *(tick e tempo proprio)*, il modo, la lunghezza minima, la deriva di `G` nella fase
esponenziale, ### **le serie dell'energia di MATERIA, VUOTO e SCAMBIO**, e gamma contro `x`.

Gira con:  python csv/_instabilita_dtau_piccolo.py
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
import _scala_salto as SS                                       # noqa: E402

EPS = float(np.finfo(float).eps)
TEMPO = 1000.0                 # il tempo totale di 29b997da (2000 tick a dtau 0.5)
ARRESTO = 0.10                 # max|delta rho| / rho_m: dichiarato nel task history
RAPPORTO = 1.0
S3 = "CAMM-MATERIA-VUOTO"
JSONL = os.path.join(RADICE, "doc", "referti_l2", "instabilita_dtau_piccolo.jsonl")
NOME_D3 = "D3 dtau 0.25"
DTAU = (0.125, 0.25)
MATERIA = ("nodo psi", "arco psi norma", "arco psi incrocio")
VUOTO = ("nodo phi", "arco phi norma", "arco phi incrocio")
SCAMBIO = ("moneta (eps h)", "N")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-66s %s   %s" % (che[:66], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def bracci():
    """### `(nome, cs acceso, salta, x, dtau)`: il controllo `P0a` per PRIMO."""
    fuori = [("I1 x 0.1 dtau 0.25", True, (), 0.1, 0.25)]
    for dt in DTAU:
        for nome, acceso, salta, x in (("C2", False, (S3,), 0.1),
                                       ("I1 x 0.01", True, (), 0.01),
                                       ("I1 x 0.1", True, (), 0.1),
                                       ("I1 x 1", True, (), 1.0),
                                       ("I2", False, (), 0.1)):
            n = "%s dtau %g" % (nome, dt)
            if n != fuori[0][0]:
                fuori.append((n, acceso, salta, x, dt))
    return fuori


def braccio(nome, acceso, salta, x, dtau):
    import composizione as CM
    import energia_pesata as EP
    import flussi_parziali as FP
    import statica_protocollo as PR
    import tick as TK
    inc, mot, st, par = JM.scena(dtau, x)
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    lc = RAPPORTO * lm
    tick = int(round(TEMPO / dtau))
    fuori = {"nome": nome, "acceso": acceso, "salta": list(salta), "x": x, "dtau": dtau,
             "tick_max": tick, "lambda_m": lm, "rho_m": rm, "lambda_c": lc,
             "cs_m": lm / (lm + lc) if acceso else 1.0}
    if acceso:
        FP.accendi_cs(mot, lc, st)
    rho, lam, G, parti, al_bit = [], [], [], [], [True]

    def foto(s):
        rho.append(mot.densita_materia(s).copy())
        lam.append(mot.densita_vuoto(s).copy())
        G.append(float(EP.g_dello_stato(mot, s, par)))
        pn, pa, pz = SS.termini(mot, s, par)
        rn, ra = EP.termini_di_h(mot, s, par)
        al_bit[0] &= bool(np.array_equal(pn, rn) and np.array_equal(pa, ra))
        parti.append((sum(pz[k] for k in MATERIA), sum(pz[k] for k in VUOTO),
                      sum(pz[k] for k in SCAMBIO)))
    foto(st)
    fuori["non_converge"] = None
    try:
        for _t in range(tick):
            if acceso:
                TK.tick_con_cs(st, mot, par, lc, salta)
            else:
                TK.percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))
            foto(st)
            if float(np.max(np.abs(rho[-1] - rm))) > ARRESTO * rm:
                break
    except AssertionError as e:
        fuori["non_converge"] = {"tick": len(rho), "lam_min": float(np.min(lam[-1])),
                                 "lambda_c": lc, "msg": str(e)[:120]}
    rho, lam, G = np.array(rho), np.array(lam), np.array(G)
    fuori["tick_fatti"] = int(rho.shape[0] - 1)
    fuori["al_bit"] = al_bit[0]
    if rho.shape[0] > 1:
        fuori["m1_rho_ulp"] = float(np.max(np.abs(rho[1] - rho[0]))) / (EPS * rm)
        fuori["m1_lam_ulp"] = float(np.max(np.abs(lam[1] - lam[0]))) / (EPS * lm)
    mr = np.max(np.abs(rho - rm), axis=1)
    ml = np.max(np.abs(lam - lm), axis=1)
    fuori["m_rho"] = [float(v) for v in mr]
    fuori["m_lam"] = [float(v) for v in ml]
    fuori["G"] = [float(v) for v in G]
    fuori["parti"] = [list(p) for p in parti]
    # ### l'escursione relativa di H (le tre parti, non pesate) nei primi 10 di tempo
    hh = np.array([sum(p) for p in parti])
    n10 = min(len(hh), int(round(10.0 / dtau)) + 1)
    fuori["escursione_rel_T10"] = float(np.max(np.abs(hh[:n10] - hh[0]))) / abs(hh[0])
    # ### la fase esponenziale: fino a max|delta rho| = 1% di rho_m
    fine = len(mr) - 1
    for t in range(len(mr)):
        if mr[t] >= IV.SOGLIA_PICCOLA * rm:
            fine = t
            break
    cresc = float(mr[fine] / rm)
    dg = float(abs(G[fine] - G[0]) / abs(G[0])) if G[0] else float("nan")
    d = [parti[fine][i] - parti[0][i] for i in range(3)]
    den = sum(abs(v) for v in d)
    fuori["fase"] = {"fine": int(fine), "crescita": cresc, "dG_rel": dg,
                     "rapporto_G": dg / cresc if cresc > 0 else None,
                     "D_materia": d[0], "D_vuoto": d[1], "D_scambio": d[2],
                     "compensazione": abs(sum(d)) / den if den > 0 else None}
    for chiave, m, scala, campi, centro in (("rho", mr, rm, rho, rm),
                                            ("lam", ml, lm, lam, lm)):
        g, b, t0, t1 = IV.gamma_del_tratto(m, scala)
        r = {"gamma": g, "barra": b, "T0": t0, "T1": t1,
             "zeri": int(np.sum(np.asarray(m)[t0:t1] == 0.0))}
        t1c = min(t1, campi.shape[0] - 1)
        w = IV.onda(campi[t1c] - centro, PR.LATI)
        r["onda"] = {"tick": t1c, "lambda": w[0], "kx": w[1], "ky": w[2], "frazione": w[3]}
        if g is not None and not r["zeri"]:
            r["gamma_k"] = JM.gamma_k(campi[t0] - centro, campi[t1c] - centro, t0, t1c,
                                      PR.LATI)
        fuori[chiave] = r
    return fuori


def d3_di_ieri():
    with io.open(JM.JSONL, encoding="utf-8") as f:
        for riga in f:
            b = json.loads(riga)
            if b.get("nome") == NOME_D3:
                return b
    raise AssertionError("il braccio `%s` non e' nel jsonl di 29b997da" % NOME_D3)


def kpi(o):
    import statica_protocollo as PR
    n = int(abs(o["kx"]) == PR.LATI[0] // 2) + int(abs(o["ky"]) == PR.LATI[1] // 2)
    return {2: "k = pi in ENTRAMBE", 1: "k = pi in UNA", 0: "NON k = pi"}[n]


def stampa_braccio(b, ts):
    print("  %-22s tick %d/%d  cs_m %.3f  escursione rel. di H (T 10) %.3e%s"
          % (b["nome"], b["tick_fatti"], b["tick_max"], b["cs_m"], b["escursione_rel_T10"],
             "" if not b["non_converge"] else
             "   ### NON CONVERGE al tick %d (Lambda min %.3e): il braccio si chiude li'"
             % (b["non_converge"]["tick"], b["non_converge"]["lam_min"])))
    for che in ("rho", "lam"):
        r = b[che]
        o = r["onda"]
        modo = "modo (%d,%d) lambda %.2f %.2f, %s" % (o["kx"], o["ky"], o["lambda"],
                                                      o["frazione"], kpi(o))
        if r["gamma"] is None:
            print("      %-4s tratto troppo corto (T1 %d)   %s" % (che, r["T1"], modo))
            continue
        if r["zeri"]:
            print("      %-4s zero esatto nel tratto: punto fisso al bit, NON cresce   %s"
                  % (che, modo))
            continue
        s = b["dtau"] * b["cs_m"]
        instab = r["gamma"] >= ts * r["barra"]
        print("      %-4s gamma %+.4e +- %.1e (%6.1f barre) per tick, %+.4e tempo proprio  %-9s %s"
              % (che, r["gamma"], r["barra"], r["gamma"] / r["barra"], r["gamma"] / s,
                 "INSTABILE" if instab else "no", modo))
        if instab and r.get("gamma_k"):
            sopra = [(q, lam_) for q, lam_, med, bar, _n in r["gamma_k"] if med >= ts * bar]
            tutti = len(sopra) == len(r["gamma_k"])
            print("           anelli sopra la soglia %d su %d; %s"
                  % (len(sopra), len(r["gamma_k"]),
                     "NESSUNA lunghezza minima (crescono tutti)" if tutti else
                     "la lunghezza minima: lambda %.2f" % min(l_ for _q, l_ in sopra)
                     if sopra else "nessun anello sopra"))
    f = b["fase"]
    print("      la fase esponenziale fino al tick %d: max|drho|/rho_m %.3e, |dG/G| %.3e,"
          " rapporto %s" % (f["fine"], f["crescita"], f["dG_rel"],
                            "%.3e" % f["rapporto_G"] if f["rapporto_G"] is not None else "-"))
    print("      l'energia: D_materia %+.4e  D_vuoto %+.4e  D_scambio %+.4e  ->"
          " compensazione %s (0 esatta, 1 nessuna)"
          % (f["D_materia"], f["D_vuoto"], f["D_scambio"],
             "%.3e" % f["compensazione"] if f["compensazione"] is not None else "-"))
    sys.stdout.flush()


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    import statica_protocollo as PR
    ts = JM.t_soglia()
    print("=" * 100)
    print("L'INSTABILITA' DELLA MATERIA UNIFORME, RIFATTA A dtau 0.125 -- una misura")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la materia uniforme (29b997da): lati %s, VUOTO %.1f, rapporto %g, SOLO rumore"
          " d'arrotondamento" % (PR.LATI, PR.VUOTO, RAPPORTO))
    print("  il passo: %d pezzi, impronta %s; dtau in %s; tempo totale %g; arresto a"
          " max|drho| > %g rho_m" % (len(CM.ORDINE), CM.IMPRONTA, DTAU, TEMPO, ARRESTO))
    print("  la soglia: t di Student al %.2f%% con %d gradi = %.3f barre; gamma contro x:"
          " 3 punti, NESSUN test (dichiarato)" % (100 * JM.COPERTURA, IV.BLOCCHI - 1, ts))
    print("  i bracci si salvano mentre corrono in %s" % os.path.relpath(JSONL, RADICE))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    bb = {}
    d3 = d3_di_ieri()
    for nome, acceso, salta, x, dt in bracci():
        t0 = time.time()
        b = braccio(nome, acceso, salta, x, dt)
        bb[nome] = b
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(b) + "\n")
        print("### %s   [%.0f s]" % (nome, time.time() - t0))
        ok = esito("P0b %s: i termini di H al bit a ogni tick" % nome, b["al_bit"])
        if "m1_rho_ulp" in b:
            ok &= esito("M1 %s: il primo tick entro 256 ulp" % nome,
                        max(b["m1_rho_ulp"], b["m1_lam_ulp"]) <= JM.ULP_BANDA,
                        "rho %.1f, Lambda %.1f ulp" % (b["m1_rho_ulp"], b["m1_lam_ulp"]))
        if nome == "I1 x 0.1 dtau 0.25":
            n = len(b["m_rho"])
            ok &= esito("P0a I1 x 0.1 dtau 0.25 = D3 di 29b997da AL BIT (%d tick)" % (n - 1),
                        b["m_rho"] == d3["m_rho"][:n] and b["G"] == d3["G"][:n])
        if not ok:
            print("### STOP: una prova e' caduta")
            return 1
        stampa_braccio(b, ts)
    print("-" * 100)
    print("### C2: LA SOLA CAMMINATA (senza %s)" % S3)
    for dt in DTAU:
        b = bb["C2 dtau %g" % dt]
        r = b["rho"]
        cresce = (r["gamma"] is not None and not r["zeri"] and r["gamma"] >= ts * r["barra"])
        print("  dtau %-6g %s" % (dt, "CRESCE: il difetto e' nella camminata" if cresce else
                                  "NON cresce: l'instabilita' nasce dall'accoppiamento S3"))
    print("### I1/I2: gamma(rho) in TEMPO PROPRIO, dtau 0.125 contro 0.25")
    for nome in ("I1 x 0.01", "I1 x 0.1", "I1 x 1", "I2"):
        a, c = bb["%s dtau 0.125" % nome], bb["%s dtau 0.25" % nome]
        ra, rc = a["rho"], c["rho"]
        if ra["gamma"] is None or rc["gamma"] is None or ra["zeri"] or rc["zeri"]:
            print("  %-10s non confrontabile (un tratto manca)" % nome)
            continue
        sa, sc = a["dtau"] * a["cs_m"], c["dtau"] * c["cs_m"]
        ga, gc = ra["gamma"] / sa, rc["gamma"] / sc
        bar = float(np.hypot(ra["barra"] / sa, rc["barra"] / sc))
        print("  %-10s 0.125: %+.4e   0.25: %+.4e   differenza %.1f barre combinate -> %s"
              % (nome, ga, gc, abs(ga - gc) / bar,
                 "COINCIDE entro la soglia" if abs(ga - gc) <= ts * bar else "NON coincide"))
    print("### I1: gamma(rho) per tick contro x (3 punti: nessun test, i numeri)")
    for dt in DTAU:
        g = [bb["I1 x %s dtau %g" % (x, dt)]["rho"]["gamma"] for x in ("0.01", "0.1", "1")]
        if any(v is None or v <= 0 for v in g):
            print("  dtau %-6g %s" % (dt, g))
            continue
        p = float(np.polyfit(np.log([0.01, 0.1, 1.0]), np.log(g), 1)[0])
        print("  dtau %-6g gamma %s   rapporti a x 0.1: %s   pendenza in log x %.3f"
              % (dt, " ".join("%.4e" % v for v in g),
                 " ".join("%.3f" % (v / g[1]) for v in g), p))
    print("=" * 100)
    print("### %d/%d prove passate. NESSUNA LETTURA OLTRE QUELLE FISSATE. LINEARE e Lambda_c"
          " FERMI." % tuple(OK))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
