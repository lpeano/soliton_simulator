# -*- coding: utf-8 -*-
r"""**LO STATO FINALE: DOVE VA LA MATERIA UNIFORME DOPO L'INSTABILITA'** *(la dinamica COMPLETA)*.

> ### ⛔ **Il task history e' `2026-10-22_stato_finale.md`**: le letture, le fasce, i grumi, il tempo sono fissati
> li', ### **prima dei numeri.** ### **Una misura: nessun file del nucleo si tocca, nessuna cura.**

## UN BRACCIO = (legge, geometria), con le DUE TAGLIE e i DUE SEMI
`R2Q`, `R1Q` *(quadrato)*, `R2T`, `R1T` *(triangoli, `SN`)*; lato `32` `dtau 0.125` e lato `64` `dtau 0.0625`; semi
`1` e `2`; rumore complesso `1e-10` relativo su `psi_h` e `phi_h`; ### **fino a `tau = 250`** di tempo proprio.

Gira con:  python csv/_stato_finale.py --braccio R2Q      (e R1Q, R2T, R1T: un referto per braccio)
           python csv/_stato_finale.py --sintesi          (la sintesi dai quattro jsonl)
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

BRACCI = {"R2Q": ("R2", "Q"), "R1Q": ("R1", "Q"), "R2T": ("R2", "T"), "R1T": ("R1", "T")}
TAGLIE = ((32, 0.125), (64, 0.0625))
SEMI = (1, 2)
RUMORE = 1e-10
TAU_FINE = 250.0
LUNGHE, RETICOLO = 0.25 * np.pi, 0.75          # |k| < 0.25 pi; r(k) >= 0.75
SATURA, DEGENERA = 0.10, 0.50
ARCHI, FISICA, TOLL_PROVA = 1.0, 2.0, 0.20
CARTELLA = os.path.join(RADICE, "doc", "referti_l2")
OSS = ("lunghe", "banda", "reticolo", "max_rel", "n_max", "L_g")


def griglia_di(geo):
    import _triangoli as T
    return T.QUADRATO if geo == "Q" else T.TRIANGOLI


def fasce(geo, lato):
    """### Per ogni `(m_x, m_y)`: `|k|` e la coordinata nella zona `r(k)`; le maschere delle tre fasce."""
    import _stabilita_triangoli as ST
    if geo == "Q":
        f = np.fft.fftfreq(lato) * lato
        kx, ky = np.meshgrid(2 * np.pi * f / lato, 2 * np.pi * f / lato, indexing="ij")
        modk = np.sqrt(kx ** 2 + ky ** 2)
        r = np.maximum(np.abs(kx), np.abs(ky)) / np.pi
    else:
        kv, _lab, _M, _K, _d = ST.zona(lato)
        modk = np.linalg.norm(kv, axis=-1)
        mM = 2.0 * np.pi / np.sqrt(3.0)
        dirs = [np.array([np.cos(np.deg2rad(30 + 60 * i)), np.sin(np.deg2rad(30 + 60 * i))])
                for i in range(6)]
        r = np.max(np.stack([kv @ d for d in dirs]), axis=0) / mM
    lunghe = modk < LUNGHE
    retic = (r >= RETICOLO) & ~lunghe
    banda = ~lunghe & ~retic
    lunghe = lunghe.copy()
    lunghe[0, 0] = False                         # k = 0 non e' una fluttuazione
    return modk, lunghe, banda, retic


def osserva(rho, lato, modk, ml, mb, mr, ii, jj):
    d = rho - np.mean(rho)
    P = np.abs(np.fft.fft2(d.reshape(lato, lato))) ** 2
    P[0, 0] = 0.0
    tot = float(P.sum())
    fr = [float(P[m].sum()) / tot if tot > 0 else 0.0 for m in (ml, mb, mr)]
    mx = np.ones(rho.shape, dtype=bool)
    np.logical_and.at(mx, ii, rho[ii] > rho[jj])
    np.logical_and.at(mx, jj, rho[jj] > rho[ii])
    nmax = int(mx.sum())
    km = float((P * modk).sum() / tot) if tot > 0 else 0.0
    return {"lunghe": fr[0], "banda": fr[1], "reticolo": fr[2],
            "max_rel": float(np.max(rho) / np.mean(rho)), "n_max": nmax,
            "L_g": float(np.sqrt(rho.size / nmax)) if nmax else float("inf"),
            "L_spettro": float(2.0 * np.pi / km) if km > 0 else float("inf")}


def corsa(legge, geo, lato, dtau, seme):
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import _triangoli as T
    import energia_pesata as EP
    import flussi_parziali as FP
    gr = griglia_di(geo)
    inc, mot, st, par = ST.scena(gr, "Q" if geo == "Q" else "SN", lato, dtau)
    ii, jj, _nn = T.toro_spostamenti((lato, lato), gr[0])
    modk, ml, mb, mr = fasce(geo, lato)
    rng = np.random.default_rng(seme)
    for k in ("psi_h", "phi_h"):
        v = st[k]
        sc = float(np.max(np.abs(v)))
        v += RUMORE * sc * (rng.standard_normal(v.shape) + 1j * rng.standard_normal(v.shape)) / np.sqrt(2.0)
    acceso = legge == "R1"
    lm = float(np.mean(mot.densita_vuoto(st)))
    lc = SL.RAPPORTO * lm
    if acceso:
        FP.accendi_cs(mot, lc, st)
    n0p = float(np.sum(np.abs(st["psi_h"]) ** 2))
    n0f = float(np.sum(np.abs(st["phi_h"]) ** 2))
    g0 = EP.g_dello_stato(mot, st, par)
    serie, tau, prossimo, s_max, ferma, t = [], 0.0, 0.0, 0.0, None, 0
    t0 = time.time()
    while tau < TAU_FINE - 1e-9:
        if tau >= prossimo - 1e-9:
            rho = mot.densita_materia(st).copy()
            if not np.all(np.isfinite(rho)):
                ferma = "NaN in rho a tau %.2f" % tau
                break
            o = osserva(rho, lato, modk, ml, mb, mr, ii, jj)
            o.update({"tau": tau, "tick": t,
                      "d_norma_psi": float(np.sum(np.abs(st["psi_h"]) ** 2)) / n0p - 1.0,
                      "d_norma_phi": float(np.sum(np.abs(st["phi_h"]) ** 2)) / n0f - 1.0,
                      "d_G": (EP.g_dello_stato(mot, st, par) - g0) / abs(g0),
                      "s_max": s_max, "avvisi": int(mot.avvisi_omega)})
            serie.append(o)
            prossimo += 1.0
        try:
            SL.passo(st, mot, par, acceso, (), lc)
        except Exception as e:                                # noqa: BLE001
            ferma = "%s a tau %.2f: %s" % (type(e).__name__, tau, str(e)[:160])
            break
        t += 1
        s_max = max(s_max, float(np.max(FP.dtau_nodo(mot))) / float(FP.dtau_rif(mot)))
        tau += dtau * (float(np.mean(mot.cs)) if acceso else 1.0)
    return {"legge": legge, "geo": geo, "lato": lato, "dtau": dtau, "seme": seme, "tick": t,
            "tau_fine": tau, "ferma": ferma, "secondi": time.time() - t0, "G0": g0, "serie": serie}


def leggi_corsa(c):
    """### Le letture del task history, sull'ultimo terzo."""
    s = c["serie"]
    T_ = c["tau_fine"]
    ult = [o for o in s if o["tau"] >= 2.0 * T_ / 3.0 - 1e-9]
    meta = 5.0 * T_ / 6.0
    a = [o for o in ult if o["tau"] < meta]
    b = [o for o in ult if o["tau"] >= meta]
    out = {"medie": {}, "cambio": {}}
    for q in OSS + ("L_spettro",):
        out["medie"][q] = float(np.mean([o[q] for o in ult])) if ult else float("nan")
    for q in OSS:
        ma = float(np.mean([o[q] for o in a])) if a else float("nan")
        mb = float(np.mean([o[q] for o in b])) if b else float("nan")
        out["cambio"][q] = abs(mb - ma) / abs(ma) if ma else float("inf")
    out["satura"] = bool(ult) and all(v < SATURA for v in out["cambio"].values())
    out["degenera"] = c["ferma"] is not None or out["medie"]["reticolo"] > DEGENERA
    out["deriva"] = {q: float(max(abs(o[q]) for o in s)) for q in ("d_norma_psi", "d_norma_phi", "d_G")}
    out["s_max"] = float(max(o["s_max"] for o in s)) if s else 0.0
    out["avvisi"] = int(s[-1]["avvisi"]) if s else 0
    return out


def stampa_corsa(c, L):
    print("  %s lato %d dtau %g seme %d: %d tick, tau %.2f, %.0f s%s" % (
        c["legge"] + c["geo"], c["lato"], c["dtau"], c["seme"], c["tick"], c["tau_fine"], c["secondi"],
        ("  ### SI FERMA: %s" % c["ferma"]) if c["ferma"] else ""))
    m, ch = L["medie"], L["cambio"]
    print("      ultimo terzo: lunghe %.3f  banda %.3f  reticolo %.3f;  max rho/<rho> %.3f;  massimi %.1f;"
          "  L_g %.3f archi;  L_spettro %.3f" % (m["lunghe"], m["banda"], m["reticolo"], m["max_rel"],
                                                 m["n_max"], m["L_g"], m["L_spettro"]))
    print("      cambio fra le due meta': %s  -> %s;  %s" % (
        "  ".join("%s %.3f" % (q, ch[q]) for q in OSS), "SATURA" if L["satura"] else "NON SATURA",
        "### DEGENERA" if L["degenera"] else "non degenera"))
    print("      conservazione (massimo scarto relativo): norma psi %.2e  norma phi %.2e  G %.2e;  cono s"
          " max %.4f;  avvisi del punto fisso %d" % (L["deriva"]["d_norma_psi"], L["deriva"]["d_norma_phi"],
                                                    L["deriva"]["d_G"], L["s_max"], L["avvisi"]))
    sys.stdout.flush()


def prova(Ls):
    """### `L_g(64)/L_g(32)` con la media sui semi: `(a)` archi, `(b)` fisica, `(c)` non decidibile."""
    l32 = float(np.mean([L["medie"]["L_g"] for (lato, _s), L in Ls.items() if lato == 32]))
    l64 = float(np.mean([L["medie"]["L_g"] for (lato, _s), L in Ls.items() if lato == 64]))
    q = l64 / l32
    if abs(q - ARCHI) <= TOLL_PROVA * ARCHI:
        v = "(a) FISSA IN ARCHI -> ARTEFATTO DEL RETICOLO"
    elif abs(q - FISICA) <= TOLL_PROVA * FISICA:
        v = "(b) FISSA IN UNITA' FISICHE -> FISICA"
    else:
        v = "(c) NE' L'UNA NE' L'ALTRA -> NON DECIDIBILE"
    return l32, l64, q, v


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    if "--sintesi" in argv:
        return sintesi()
    nome = argv[argv.index("--braccio") + 1]
    legge, geo = BRACCI[nome]
    jl = os.path.join(CARTELLA, "stato_finale_%s.jsonl" % nome)
    print("=" * 100)
    print("LO STATO FINALE, braccio %s: %s sul %s" % (nome, legge, "QUADRATO" if geo == "Q" else "TOROIDE TRIANGOLARE (SN)"))
    print("=" * 100)
    print("  la materia uniforme x 0.1, vuoto 1; %s; il passo %d pezzi, impronta %s" % (
        "cs ACCESO, Lambda_c = 1 * Lambda medio" if legge == "R1" else "cs SPENTO", len(CM.ORDINE), CM.IMPRONTA))
    print("  taglie %s; semi %s; rumore %g relativo; tau fine %g (tempo proprio); osservabili a ogni unita'"
          % (TAGLIE, SEMI, RUMORE, TAU_FINE))
    print("  fasce: lunghe |k| < 0.25 pi, reticolo r(k) >= %g, banda il resto; L_g = sqrt(n / massimi locali)"
          " in archi" % RETICOLO)
    print("-" * 100)
    sys.stdout.flush()
    io.open(jl, "w", encoding="utf-8").close()
    Ls = {}
    for lato, dtau in TAGLIE:
        for seme in SEMI:
            c = corsa(legge, geo, lato, dtau, seme)
            L = leggi_corsa(c)
            stampa_corsa(c, L)
            Ls[(lato, seme)] = L
            with io.open(jl, "a", encoding="utf-8") as f:
                f.write(json.dumps({"corsa": c, "letture": L}) + "\n")
    l32, l64, q, v = prova(Ls)
    print("-" * 100)
    print("  ### LA PROVA CHE DECIDE: L_g lato 32 %.3f, lato 64 %.3f archi; rapporto %.3f -> %s" % (l32, l64, q, v))
    with io.open(jl, "a", encoding="utf-8") as f:
        f.write(json.dumps({"prova": {"L32": l32, "L64": l64, "rapporto": q, "verdetto": v}}) + "\n")
    print("=" * 100)
    return 0


def sintesi():
    fuori = os.path.join(CARTELLA, "stato_finale.jsonl")
    print("=" * 100)
    print("LO STATO FINALE: LA SINTESI DEI QUATTRO BRACCI")
    print("=" * 100)
    righe = []
    for nome in BRACCI:
        jl = os.path.join(CARTELLA, "stato_finale_%s.jsonl" % nome)
        if not os.path.exists(jl):
            print("  %s: ### MANCA il referto" % nome)
            continue
        Ls, pr = [], None
        for r in io.open(jl, encoding="utf-8"):
            w = json.loads(r)
            if "letture" in w:
                Ls.append((w["corsa"]["lato"], w["corsa"]["seme"], w["letture"], w["corsa"]["ferma"]))
            if "prova" in w:
                pr = w["prova"]
        for lato, seme, L, ferma in Ls:
            print("  %s lato %d seme %d: %s, %s; reticolo %.3f; L_g %.3f; deriva G %.2e%s" % (
                nome, lato, seme, "SATURA" if L["satura"] else "NON SATURA",
                "DEGENERA" if L["degenera"] else "non degenera", L["medie"]["reticolo"], L["medie"]["L_g"],
                L["deriva"]["d_G"], ("; si ferma: " + ferma) if ferma else ""))
        if pr:
            print("  %s: ### LA PROVA: %.3f / %.3f = %.3f -> %s" % (nome, pr["L64"], pr["L32"], pr["rapporto"],
                                                                  pr["verdetto"]))
        righe.append({"braccio": nome, "corse": [[a, b, L] for a, b, L, _f in Ls], "prova": pr})
        print("-" * 100)
    with io.open(fuori, "w", encoding="utf-8") as f:
        for r in righe:
            f.write(json.dumps(r) + "\n")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
