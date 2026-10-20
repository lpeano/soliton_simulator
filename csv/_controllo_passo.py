# -*- coding: utf-8 -*-
r"""**DUE CONTROLLI DEL PASSO SULLA MATERIA UNIFORME** — *una misura, nessun codice di fisica.*

> ### ⛔ **Il task history e' `2026-10-20_controllo_passo_materia_uniforme.md`** *(`5f5e8aa7`)*,
> coi criteri fissati prima. Decisione di Luca del `2026-10-20` alle `09:12`: ### **prima di
> qualunque interpretazione dell'instabilita' di `29b997da`, il passo.**
> ### **`LINEARE`, `Lambda_c` e ogni lettura «alla Jeans» restano FERMI.**

## ⛔ `P0` — LE PROVE DELLO STRUMENTO *(se una cade: STOP)*

`P0a` il rivelatore del periodo `2` su due serie sintetiche *(una deve scattare, una no)* ·
`P0b` ### **la banda `B`**: il braccio `k = 1` di `C1` di strada `(d)` rifatto, contro il
referto `c1_tetto_omega.txt`, e `B = escursione / |G(0)|` · `P0c` ### **i `21` campioni di `G`
del braccio `D2` di `29b997da` riprodotti AL BIT**, e i campioni a meta' tick che ### **non
toccano** quelli a tick intero.

## ⭐ `C1` — `G` E `H` A `CS` SPENTO, TICK PER TICK

La scena di `D2`, `20` tick; a ogni tick intero e a ogni meta' tick ### **`G`** *(`g_dello_stato`)*
e ### **`H`** *(`_misura_mb2.h_tot`, da zero)*. ### **Conserva** se l'escursione relativa sui tick
interi e' `<= B`; ### **periodo `2`** se le differenze alternano di segno sopra la banda. ### **Il
caso che deve riuscire: la scena di `M-B2`.** ### **Se `C1` cade, `C2` NON gira.**

## ⭐ `C2` — LA SOLA CAMMINATA, SENZA `CAMM-MATERIA-VUOTO`

La scena di `D2`, `2000` tick, `salta = ("CAMM-MATERIA-VUOTO",)`; ### **il braccio `0`**
*(`salta = ()`)* ### **riproduce `D2` al bit.** «Cresce» se `gamma >= t * barra`.

Gira con:  python csv/_controllo_passo.py
"""
import io
import json
import os
import re
import sys

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
X = 0.1                    # la scena di `D2`
DTAU = 0.5
TICK_C1 = 20               # dichiarati nel task history
TICK_C2 = 2000             # come `D2` di `29b997da`
NOME_D2 = "D2 cs SPENTO"
S3 = "CAMM-MATERIA-VUOTO"
REF_C1 = os.path.join(RADICE, "doc", "referti_l2", "c1_tetto_omega.txt")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "controllo_passo.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-66s %s   %s" % (che[:66], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def stop(perche):
    print("=" * 100)
    print("### STOP: %s" % perche)
    print("### NESSUNA INTERPRETAZIONE FISICA. LINEARE e Lambda_c FERMI.")
    print("=" * 100)
    return 1


# =====================================================================================
#   I DUE CRITERI DI C1, come funzioni (le prova P0a)
# =====================================================================================
def escursione_rel(H):
    H = np.asarray(H, dtype=float)
    return float(np.max(np.abs(H[1:] - H[0]))) / abs(H[0])


def periodo2(H, B):
    """### Per ogni `t = 0..len-3`: `dH_t dH_(t+1) < 0` e `|dH_t| > B |H(0)|`."""
    H = np.asarray(H, dtype=float)
    d = np.diff(H)
    soglia = B * abs(H[0])
    for t in range(len(d) - 1):
        if not (d[t] * d[t + 1] < 0 and abs(d[t]) > soglia):
            return False
    return True


# =====================================================================================
#   P0b: LA BANDA
# =====================================================================================
def banda():
    import _misura_hw as HW
    import _misura_mb2 as MB2
    import _misura_strada_d as SD
    import deriva as DV
    import energia_pesata as EP
    import flussi_parziali as FP
    quanti = int(round(MB2.TEMPO / DTAU))
    e, giri_cs, giri_om = SD.corsa(DTAU, quanti, True, "centro", 1)
    inc, mot, st, par = DV.scena(MB2.NN, MB2.SEME, DTAU, norma=MB2.NORMA,
                                 vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)
    st["psi_h"][...], st["phi_h"][...] = HW.stato_non_uniforme()
    lc = float(np.mean(mot.densita_vuoto(st)))
    FP.accendi_cs(mot, lc, st)
    g0 = float(EP.g_dello_stato(mot, st, par))
    return e, g0, quanti, giri_cs, giri_om


def dal_referto():
    """### L'escursione `k = 1` di `C1` col termine, ### **letta dal file**, com'e' stampata."""
    testo = io.open(REF_C1, encoding="utf-8").read()
    i = testo.index("### `C1` LA PENDENZA DI `G` con `cs` DINAMICO, COL TERMINE")
    m = re.search(r"^\s+1\s+0\.500000\s+16\s+(\S+)", testo[i:], re.M)
    return m.group(1)


# =====================================================================================
#   C1: I CAMPIONI
# =====================================================================================
def campione(inc, mot, st, par):
    import _misura_mb2 as MB2
    import energia_pesata as EP
    g = float(EP.g_dello_stato(mot, st, par))
    h = float(MB2.h_tot(inc, mot, st, par))
    # ### la scala della seconda fonte: la SOMMA DEI VALORI ASSOLUTI dei termini, cioe'
    # ### ### **i tetti che `termini_di_h` ha appena scritto nei buffer del motore**
    tn = mot._b("ep_tetto_nodo", (inc.n,), float)
    ta = mot._b("ep_tetto_arco", (inc.m,), float)
    return g, h, float(np.sum(tn)) + float(np.sum(ta))


def serie_c1(inc, mot, st, par, tick, meta_tick):
    import tick as TK
    intero, mezzo = [campione(inc, mot, st, par)], []
    meta = TK.meta_del_palindromo()
    for _t in range(tick):
        if meta_tick:
            copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
            TK.percorri_tick(copia, mot, par, (), None, meta)
            mezzo.append(campione(inc, mot, copia, par))
        TK.tick(st, mot, par)
        intero.append(campione(inc, mot, st, par))
    return intero, mezzo


def scena_mb2():
    import _misura_mb2 as MB2
    import deriva as DV
    return DV.scena(MB2.NN, MB2.SEME, DTAU, norma=MB2.NORMA,
                    vuoto_modulo=MB2.VUOTO_MODULO, su2=MB2.SU2)


def stampa_serie(intero, mezzo):
    print("     t       G (g_dello_stato)       H (h_tot, da zero)      |G-H|/scala (ulp)")
    for t in range(len(intero)):
        g, h, s = intero[t]
        print("     %-6s  %+.12e   %+.12e   %.1f" % (t, g, h, abs(g - h) / (EPS * s)))
        if t < len(mezzo):
            g, h, s = mezzo[t]
            print("     %-6s  %+.12e   %+.12e   %.1f" % ("%d.5" % t, g, h, abs(g - h) / (EPS * s)))


def seconda_fonte(intero, mezzo):
    import _misura_hw as HW
    peggio = max(abs(g - h) / (EPS * s) for g, h, s in list(intero) + list(mezzo))
    return peggio, HW.ULP_SECONDA_FONTE


# =====================================================================================
#   C2: LA CAMMINATA
# =====================================================================================
def corsa_c2(salta):
    import composizione as CM
    import energia_pesata as EP
    import tick as TK
    inc, mot, st, par = JM.scena(DTAU, X)
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    rho, lam, G = [], [], []

    def foto():
        rho.append(mot.densita_materia(st).copy())
        lam.append(mot.densita_vuoto(st).copy())
        G.append(float(EP.g_dello_stato(mot, st, par)))
    foto()
    for _t in range(TICK_C2):
        TK.percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))
        foto()
    rho, lam = np.array(rho), np.array(lam)
    return {"rho_m": rm, "lambda_m": lm, "rho": rho, "lam": lam, "G": G,
            "m_rho": np.max(np.abs(rho - rm), axis=1),
            "m_lam": np.max(np.abs(lam - lm), axis=1)}


def fit(m, scala, campi, centro, ts):
    import statica_protocollo as PR
    fuori = {}
    g, b, t0, t1 = IV.gamma_del_tratto(m, scala)
    fuori.update({"T0": t0, "T1": t1})
    zeri = int(np.sum(np.asarray(m)[t0:t1] == 0.0))
    fuori["zeri"] = zeri
    if zeri:
        # ### ⚠ **`log` non esiste**: lo stato uniforme e' un punto fisso al bit
        fuori["verdetto"] = "zero esatto: punto fisso al bit"
        fuori["cresce"] = False
    elif g is None:
        fuori["verdetto"] = "tratto troppo corto"
        fuori["cresce"] = None
    else:
        fuori.update({"gamma": g, "barra": b, "barre": g / b if b else float("inf")})
        fuori["cresce"] = bool(g >= ts * b)
        fuori["verdetto"] = "CRESCE" if fuori["cresce"] else "non cresce"
    t1c = min(t1, campi.shape[0] - 1)
    w = IV.onda(campi[t1c] - centro, PR.LATI)
    fuori["onda"] = {"tick": t1c, "lambda": w[0], "kx": w[1], "ky": w[2], "frazione": w[3]}
    if fuori.get("cresce"):
        gk = JM.gamma_k(campi[t0] - centro, campi[t1c] - centro, t0, t1c, PR.LATI)
        fuori["anelli"] = [q for q, _l, med, bar, _n in gk if med >= ts * bar]
    return fuori


def riga_fit(nome, che, r, dtau):
    o = r["onda"]
    modo = "modo lambda %.2f (%d,%d) %.2f al tick %d" % (o["lambda"], o["kx"], o["ky"],
                                                        o["frazione"], o["tick"])
    if "gamma" in r:
        print("  %-14s %-6s gamma %+.4e +- %.1e (%6.1f barre) per tick  %+.4e tempo proprio"
              "  %-10s %s" % (nome, che, r["gamma"], r["barra"], r["barre"],
                              r["gamma"] / dtau, r["verdetto"], modo))
    else:
        print("  %-14s %-6s %s   %s" % (nome, che, r["verdetto"], modo))
    if r.get("anelli") is not None:
        print("                        anelli |k| sopra la soglia: %s" % r["anelli"])


def d2_di_ieri():
    with io.open(JM.JSONL, encoding="utf-8") as f:
        for riga in f:
            b = json.loads(riga)
            if b.get("nome") == NOME_D2:
                return b
    raise AssertionError("il braccio `%s` non e' nel jsonl di 29b997da" % NOME_D2)


# =====================================================================================
#   MAIN
# =====================================================================================
def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _misura_mb2 as MB2
    import composizione as CM
    import energia_pesata as EP
    import statica_protocollo as PR
    ts = JM.t_soglia()
    print("=" * 100)
    print("DUE CONTROLLI DEL PASSO SULLA MATERIA UNIFORME -- una misura, nessun codice di fisica")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  la scena di D2 (29b997da): lati %s, VUOTO %.1f, x %g, dtau %g, cs SPENTO, nessuna"
          " perturbazione" % (PR.LATI, PR.VUOTO, X, DTAU))
    print("  il passo: %d pezzi, impronta %s; il mezzo tick: %d pezzi (il centro del palindromo)"
          % (len(CM.ORDINE), CM.IMPRONTA, len(CM.ORDINE) // 2))
    print("  C1: %d tick; C2: %d tick, senza %s; la soglia di Student %.3f barre"
          % (TICK_C1, TICK_C2, S3, ts))
    print("  la scena di M-B2: nn %d, seme %d, norma %s, vuoto_modulo %g, su2 %s, dtau %g"
          % (MB2.NN, MB2.SEME, MB2.NORMA, MB2.VUOTO_MODULO, MB2.SU2, DTAU))
    print("  le due fonti di H: OMEGA_H %.17g (energia_pesata), OMEGA %.17g (_misura_mb2)"
          % (EP.OMEGA_H, MB2.OMEGA))
    print("-" * 100)
    sys.stdout.flush()

    # ------------------------------------------------------------------ P0
    print("### P0: LE PROVE DELLO STRUMENTO (se una cade, STOP)")
    print("  la cadenza di 29b997da (dal sorgente): UN campione di G per tick INTERO, dopo"
          " ogni TK.tick; il primo al tick 0; nessuno a meta' tick")
    e, g0b, quanti, gcs, gom = banda()
    B = e / abs(g0b)
    rif = dal_referto()
    print("  la banda: C1 di strada (d), k = 1 (dtau %g, %d tick): escursione %.6e, |G(0)| %.6e,"
          " giri cs %d, giri Omega %d" % (DTAU, quanti, e, abs(g0b), gcs, gom))
    print("  ### B = %.6e (escursione relativa)" % B)
    p0 = True
    p0 &= esito("P0b l'escursione rifatta coincide col referto (7 cifre)",
                "%.6e" % e == rif, "rifatta %.6e, referto %s" % (e, rif))
    sint = [1.0 + 3.0 * B * (-1) ** t for t in range(TICK_C1 + 1)]
    rng = np.random.default_rng(0)
    piatta = list(1.0 + 1e-3 * B * rng.standard_normal(TICK_C1 + 1))
    p0 &= esito("P0a la serie alternante a 3B DEVE dare periodo 2", periodo2(sint, B))
    p0 &= esito("P0a la serie piatta (rumore 1e-3 B) NON deve", not periodo2(piatta, B))
    inc, mot, st, par = JM.scena(DTAU, X)
    intero_a, _ = serie_c1(inc, mot, st, par, TICK_C1, False)
    inc, mot, st, par = JM.scena(DTAU, X)
    intero, mezzo = serie_c1(inc, mot, st, par, TICK_C1, True)
    ieri = d2_di_ieri()
    Ga = [c[0] for c in intero_a]
    p0 &= esito("P0c i 21 campioni di G = D2 di 29b997da AL BIT",
                Ga == ieri["G"][:TICK_C1 + 1],
                "primi tre: %.1f %.1f %.1f" % tuple(Ga[:3]))
    p0 &= esito("P0c i campioni a meta' tick non toccano quelli a tick intero",
                [c[0] for c in intero] == Ga and [c[1] for c in intero] == [c[1] for c in intero_a])
    if not p0:
        return stop("una prova dello strumento e' caduta")
    print("-" * 100)

    # ------------------------------------------------------------------ C1, il caso che deve riuscire
    print("### C1, IL CASO CHE DEVE RIUSCIRE: la scena di M-B2, cs spento, %d tick" % TICK_C1)
    inc2, mot2, st2, par2 = scena_mb2()
    int_m, mez_m = serie_c1(inc2, mot2, st2, par2, TICK_C1, True)
    stampa_serie(int_m, mez_m)
    pf, tetto = seconda_fonte(int_m, mez_m)
    Hm = [c[1] for c in int_m]
    ok = esito("M-B2: la seconda fonte |G-H| entro %d ulp" % tetto, pf <= tetto, "%.1f ulp" % pf)
    ok &= esito("M-B2: (i) conserva, escursione relativa <= B", escursione_rel(Hm) <= B,
                "%.3e contro B %.3e" % (escursione_rel(Hm), B))
    ok &= esito("M-B2: (ii) NON periodo 2", not periodo2(Hm, B))
    if not ok:
        return stop("il caso di M-B2 non riesce: lo strumento o la banda sono sbagliati,"
                    " e nessun verdetto su C1")
    print("-" * 100)

    # ------------------------------------------------------------------ C1
    print("### C1: LA MATERIA UNIFORME DI D2, cs spento, %d tick, a tick intero e a meta' tick"
          % TICK_C1)
    stampa_serie(intero, mezzo)
    pf, tetto = seconda_fonte(intero, mezzo)
    H = [c[1] for c in intero]
    Hh = [c[1] for c in mezzo]
    print("  a meta' tick: escursione relativa da H(0) %.3e" % (
        float(np.max(np.abs(np.asarray(Hh) - H[0]))) / abs(H[0])))
    fonte = esito("C1: la seconda fonte |G-H| entro %d ulp" % tetto, pf <= tetto, "%.1f ulp" % pf)
    if not fonte:
        return stop("G e h_tot non misurano la stessa cosa sulla materia uniforme")
    c_i = esito("C1: (i) conserva, escursione relativa <= B", escursione_rel(H) <= B,
                "%.3e contro B %.3e" % (escursione_rel(H), B))
    c_ii = esito("C1: (ii) NON periodo 2", not periodo2(H, B))
    with io.open(JSONL, "w", encoding="utf-8") as f:
        f.write(json.dumps({"che": "C1", "B": B, "intero": intero, "mezzo": mezzo,
                            "mb2_intero": int_m, "mb2_mezzo": mez_m}) + "\n")
    if not (c_i and c_ii):
        return stop("C1 cade: il passo NON conserva H sulla materia uniforme -- un difetto del"
                    " passo, indipendente da cs. C2 NON gira")
    print("-" * 100)

    # ------------------------------------------------------------------ C2
    print("### C2: LA SOLA CAMMINATA, senza %s, cs spento, %d tick" % (S3, TICK_C2))
    zero = corsa_c2(())
    bit = (zero["G"] == ieri["G"] and list(map(float, zero["m_rho"])) == ieri["m_rho"]
           and list(map(float, zero["m_lam"])) == ieri["m_lam"])
    if not esito("C2 braccio 0 (salta = ()) riproduce D2 di 29b997da AL BIT", bit):
        return stop("il braccio 0 di C2 non riproduce D2")
    senza = corsa_c2((S3,))
    risultati = {}
    for nome, r in (("braccio 0", zero), ("senza S3", senza)):
        for che, m, scala, campi, centro in (
                ("rho", r["m_rho"], r["rho_m"], r["rho"], r["rho_m"]),
                ("Lambda", r["m_lam"], r["lambda_m"], r["lam"], r["lambda_m"])):
            f = fit(m, scala, campi, centro, ts)
            risultati[(nome, che)] = f
            riga_fit(nome, che, f, DTAU)
        print("  %-14s max|delta rho|/rho_m alla fine %.3e;  G: tick 0 %.6e, fine %.6e"
              % (nome, float(r["m_rho"][-1]) / r["rho_m"], r["G"][0], r["G"][-1]))
    with io.open(JSONL, "a", encoding="utf-8") as f:
        for nome, r in (("braccio 0", zero), ("senza S3", senza)):
            f.write(json.dumps({"che": "C2", "nome": nome, "G": r["G"],
                                "m_rho": [float(v) for v in r["m_rho"]],
                                "m_lam": [float(v) for v in r["m_lam"]],
                                "fit": {k[1]: v for k, v in risultati.items() if k[0] == nome}})
                    + "\n")
    cresce = risultati[("senza S3", "rho")].get("cresce")
    o = risultati[("braccio 0", "rho")]["onda"]
    print("-" * 100)
    print("### LA LETTURA, fissata nel task history:")
    if cresce:
        print("  la sola camminata CRESCE: il difetto e' nella camminata")
    elif cresce is False:
        print("  la sola camminata NON cresce: l'instabilita' nasce dall'accoppiamento S3"
              " materia-vuoto, sul modo (%d,%d) (lambda %.2f): %s"
              % (o["kx"], o["ky"], o["lambda"],
                 {2: "k = pi in ENTRAMBE le direzioni", 1: "k = pi in UNA direzione",
                  0: "NON k = pi"}[int(abs(o["kx"]) == PR.LATI[0] // 2)
                                   + int(abs(o["ky"]) == PR.LATI[1] // 2)]))
    else:
        print("  ### NON DECIDIBILE: il tratto della sola camminata e' troppo corto")
    print("=" * 100)
    print("### %d/%d prove passate. NESSUNA INTERPRETAZIONE FISICA. LINEARE e Lambda_c FERMI."
          % tuple(OK))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
