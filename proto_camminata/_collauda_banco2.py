# -*- coding: utf-8 -*-
"""IL COLLAUDO DEL BANCO `v2` — **e il BRACCIO `0` si dice in DUE PEZZI.**

> ## ⛔ **IL BRACCIO `0`:** `C ψ = i σ_y ψ*` **commuta con tutto `SU(2)`** e **INVERTE la
> ## fase `U(1)`**. Quindi: **`(i)`** nella scena **identita'** `C` commuta **AL BIT**;
> ## **`(ii)`** con un campo acceso, `C` manda la camminata **nell'ANTI-camminata**, e la
> ## simmetria e' `C(U ψ) = U_coniugata(C ψ)`.
> ### ⚠ **NON e' un fallimento: e' che la coniugazione di CARICA inverte la CARICA.**

### ⭐ **E IL BRACCIO CHE DEVE FALLIRE E' LA PROVA CHE I VERSORI SERVONO:** la scena di gauge
puro **coi versori NON ruotati** deve dare osservabili **DIVERSE**. ### **Se non le desse, i
riferimenti locali sarebbero ridondanti e il punto `1` del mandato cadrebbe.**

Gira con:  python proto_camminata/_collauda_banco2.py
"""
import io
import math
import os
import subprocess
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

EPS = float(np.finfo(float).eps)
NLN = chr(10)
SEME = 11
PASSI = 40
EPS_SPIN = 0.5

# ### i file di FISICA del banco `v2` *(questo file NOMINA le forme, quindi non si guarda)*
FISICA2 = ("geometria.py", "camminata2.py", "nonlineare2.py", "_letture2.py")
CLIP = ("np.clip", ".clip(", "np.maximum", "np.minimum", "np.fmax", "np.fmin")


def ruota_stato(psi, sc, g, fi=None):
    """Lo stato **ruotato dal gauge**: `ψ[h] → g_k ψ[h]`."""
    # ### ⛔ **LA FASE `U(1)` FA PARTE DELLA TRASFORMAZIONE, e dimenticarla e-
    # ### stato il mio primo errore qui:** `rho` e- invariante per fase, quindi
    # ### **sembrava innocuo** -- ma se le `U` della scena portano `exp(i(fi_v-fi_u))`
    # ### e lo stato **non porta `exp(i fi_k)`**, allora quello stato **NON E- il
    # ### trasformato di gauge** di `psi`, e **le fasi RELATIVE fra i nodi sono diverse.**
    # ### ✅ **E la misura lo ha detto subito:** `max|rho - rho'| = 1.2e-2` contro
    # ### una soglia di `5.3e-14`.
    out = np.empty_like(psi)
    for e in range(psi.shape[0]):
        k = int(sc["nodo"][e])
        f = 1.0 if fi is None else np.exp(1j * fi[k])
        out[e] = f * (g[k] @ psi[e])
    return out


def main():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DEL BANCO v2 -- SPIN LEGATO AL MOTO")
    print("=" * 100)
    SC._niente_simulatore()

    sc = SC.irregolare()
    r = SC.ritmi(sc, SEME)
    psi = CM.stato_casuale(sc, SEME)
    nest = 2 * sc["m"]
    gmax = int(sc["grado"].max())
    tol = PASSI * gmax * EPS * math.sqrt(CM.norma(psi))
    tolN = PASSI * nest * EPS
    ident = GE.scena_identita(sc)
    gauge = GE.scena_gauge_puro(sc, SEME)
    curva = GE.scena_curva(sc, SEME)
    SCENE = (("identita", ident), ("gauge_puro", gauge), ("curva", curva))

    # ================================================================ MATERIA
    nn = ident["n"]
    esito("### MATERIA: i versori sono UNITARI",
          float(np.max(np.abs(np.linalg.norm(nn, axis=1) - 1.0))) <= 8 * EPS,
          "### %d versori, scarto massimo da 1: %.3g"
          % (len(nn), float(np.max(np.abs(np.linalg.norm(nn, axis=1) - 1.0)))))
    # ### ⚠ **E NON SONO ANTIPODALI, e il braccio lo DICE invece di lasciarlo scoprire**
    anti = max(float(np.max(np.abs(nn[2 * a] + nn[2 * a + 1]))) for a in range(sc["m"]))
    esito("### i due versori di un arco NON sono antipodali, ed e- VOLUTO", anti > 0.1,
          "### max|n_u + n_v| = %.3f: senza `pos` non esiste <<la direzione dell-arco>>, e "
          "la relazione fra i riferimenti E- la connessione" % anti)
    tr_i = [x[1] for x in GE.olonomie(sc, ident["U"])]
    tr_g = [x[1] for x in GE.olonomie(sc, gauge["U"])]
    tr_c = [x[1] for x in GE.olonomie(sc, curva["U"])]
    esito("### MATERIA: le olonomie sono BANALI in identita- e gauge puro",
          max(abs(x - 2.0) for x in tr_i + tr_g) <= 1e-12,
          "### traccia SU(2) = 2 entro %.3g su %d cicli"
          % (max(abs(x - 2.0) for x in tr_i + tr_g), len(tr_i)))
    esito("### e NON banali nella scena CURVA", min(tr_c) < 1.0,
          "### traccia SU(2) in [%.3f, %.3f]: senza questo la lettura `O` non avrebbe "
          "materia" % (min(tr_c), max(tr_c)))

    # ================================================================ LA NORMA
    for nome, geo in SCENE:
        fine, _ = C2.corri2(psi, sc, geo, r, 1.0, EPS_SPIN, PASSI)
        d = abs(CM.norma(fine) - CM.norma(psi))
        esito("la NORMA si conserva entro `passi*n_est*eps` -- %s" % nome, d <= tolN,
              "### scarto %.3g, soglia %.3g" % (d, tolN))

    # ================================================================ IL BRACCIO 0
    a = C2.coniuga2(C2.passo2(psi, sc, ident, r, 1.0, EPS_SPIN))
    b = C2.passo2(C2.coniuga2(psi), sc, ident, r, 1.0, EPS_SPIN)
    d = float(np.max(np.abs(a - b)))
    esito("### BRACCIO 0 (i): nella scena IDENTITA- `C` COMMUTA, AL BIT", d == 0.0,
          "### max|C(U psi) - U(C psi)| = %.3g, e la derivazione diceva ESATTAMENTE 0" % d)
    for nome, geo in SCENE[1:]:
        a = C2.coniuga2(C2.passo2(psi, sc, geo, r, 1.0, EPS_SPIN))
        c = C2.passo_coniugato(C2.coniuga2(psi), sc, geo, r, 1.0, EPS_SPIN)
        dd = float(np.max(np.abs(a - c)))
        nc = float(np.max(np.abs(a - C2.passo2(C2.coniuga2(psi), sc, geo, r, 1.0,
                                               EPS_SPIN))))
        esito("### BRACCIO 0 (ii): in `%s` `C` manda nella ANTI-camminata" % nome,
              dd <= tol and nc > 1e-3,
              "### |C U - U_coniugata C| = %.3g (soglia %.3g), e |C U - U C| = %.3g: "
              "### la fase U(1) NON commuta, e deve non commutare" % (dd, tol, nc))
    cc = float(np.max(np.abs(C2.coniuga2(C2.coniuga2(psi)) + psi)))
    esito("### e `C(C psi) = -psi` AL BIT: e- la DOPPIA COPERTURA", cc == 0.0,
          "### max|C(C psi) + psi| = %.3g -- `C^2 = -I`, e non e- un difetto" % cc)

    # ================================================================ LE NON LINEARI
    for et, f, _nota in N2.LE_DUE_V2:
        peggio, meglio = 0.0, 0.0
        for _nome, geo in SCENE:
            a = C2.coniuga2(C2.passo2(psi, sc, geo, r, 1.0, EPS_SPIN, 1.0, f))
            c = C2.passo_coniugato(C2.coniuga2(psi), sc, geo, r, 1.0, EPS_SPIN, 1.0, f)
            dd = float(np.max(np.abs(a - c)))
            peggio = max(peggio, dd)
            meglio = max(meglio, dd)
        if et == "A":
            esito("### DEVE ROMPERE `C`: la fase PARI (A), in tutte le scene",
                  peggio > 1e-6,
                  "### max|C U - U_coniugata C| = %.3g: e- IL BRACCIO CHE DEVE FALLIRE la "
                  "lettura 5" % peggio)
        else:
            esito("### NON deve rompere `C`: la fase DISPARI (B), l-ELICITA-",
                  meglio <= tol,
                  "### max|C U - U_coniugata C| = %.3g, soglia %.3g" % (meglio, tol))

    # ================================================================ L'ELICITA'
    h0 = N2.elicita_nodo(psi, sc, ident)
    ruot = ruota_stato(psi, sc, gauge["g"], gauge["fi"])
    h1 = N2.elicita_nodo(ruot, sc, gauge)
    h2 = N2.elicita_nodo(ruot, sc, {"n": gauge["n_non_ruotati"]})
    d1 = float(np.max(np.abs(h0 - h1)))
    d2 = float(np.max(np.abs(h0 - h2)))
    esito("### l-ELICITA- e- INVARIANTE DI GAUGE", d1 <= tol,
          "### max|h - h'| = %.3g, soglia %.3g: `s` e `n` ruotano INSIEME" % (d1, tol))
    esito("### DEVE FALLIRE: l-elicita- SENZA ruotare i versori NON e- invariante",
          d2 > 1e-6,
          "### max|h - h''| = %.3g, cioe- %d ordini di grandezza sopra: ### **i versori "
          "NON sono ridondanti**" % (d2, int(round(math.log10(d2 / max(d1, EPS))))))

    # ================================================================ LA LETTURA G
    # ### ⭐ **LA GAUGE-INVARIANZA DELLA DINAMICA**: la densita- per nodo e- invariante,
    # ### quindi partendo dallo stato RUOTATO nella scena di gauge puro deve dare
    # ### ### **la stessa densita-** della scena identita-.
    f_i, _ = C2.corri2(psi, sc, ident, r, 1.0, EPS_SPIN, PASSI)
    f_g, _ = C2.corri2(ruot, sc, gauge, r, 1.0, EPS_SPIN, PASSI)
    dg = float(np.max(np.abs(CM.rho_nodo(f_i, sc) - CM.rho_nodo(f_g, sc))))
    esito("### LETTURA G: il gauge puro da- la STESSA densita- per nodo", dg <= tol,
          "### max|rho - rho'| = %.3g, soglia %.3g" % (dg, tol))
    senza = dict(gauge)
    senza["n"] = gauge["n_non_ruotati"]
    f_s, _ = C2.corri2(ruot, sc, senza, r, 1.0, EPS_SPIN, PASSI)
    ds = float(np.max(np.abs(CM.rho_nodo(f_i, sc) - CM.rho_nodo(f_s, sc))))
    esito("### DEVE FALLIRE: lo stesso gauge coi VERSORI NON RUOTATI", ds > 1e-6,
          "### max|rho - rho''| = %.3g: ### **e- la PROVA che i riferimenti locali "
          "servono**" % ds)

    # ================================================================ LE BANDE
    solo0 = psi.copy()
    solo0[:, 1] = 0.0
    solo0 = solo0 / math.sqrt(CM.norma(solo0))
    f0, _ = C2.corri2(solo0, sc, ident, r, 1.0, 0.0, PASSI)
    f1, _ = C2.corri2(solo0, sc, ident, r, 1.0, EPS_SPIN, PASSI)
    m0 = float(np.max(np.abs(f0[:, 1])))
    m1 = float(np.max(np.abs(f1[:, 1])))
    esito("### con `eps = 0` e identita- le componenti NON si mescolano (come il v1)",
          m0 == 0.0, "### |componente 1| = %.3g" % m0)
    esito("### e con `eps > 0` SI MESCOLANO: lo spin si lega al moto", m1 > 1e-6,
          "### |componente 1| = %.3g -- ### **e- la differenza col v1**" % m1)
    f2, _ = C2.corri2(solo0, sc, curva, r, 1.0, 0.0, PASSI)
    esito("### e con `eps = 0` ma trasporto CURVO si mescolano LO STESSO",
          float(np.max(np.abs(f2[:, 1]))) > 1e-6,
          "### |componente 1| = %.3g: ### **mescola anche il TRASPORTO**, non solo la "
          "moneta" % float(np.max(np.abs(f2[:, 1]))))

    # ================================================================ IL CONO
    d0 = SC.distanze(sc, 0)
    T = max(1, int(d0.max()) // 2)
    e0 = int(np.nonzero(sc["nodo"] == 0)[0][0])
    u1 = CM.stato_zero(sc)
    u1[e0, 0] = 1.0
    u2 = u1.copy()
    u2[e0, 0] = 1.0 + 1e-3
    g1, _ = C2.corri2(u1, sc, curva, r, 1.0, EPS_SPIN, T)
    g2, _ = C2.corri2(u2, sc, curva, r, 1.0, EPS_SPIN, T)
    dif = np.abs(g1 - g2).sum(axis=1)
    fuori = dif[d0[sc["nodo"]] > T]
    esito("### IL CONO con TRASPORTO: oltre %d archi ZERO ESATTO" % T,
          fuori.size > 0 and float(np.max(fuori)) == 0.0,
          "### max fuori = %.3g su %d estremita-"
          % (float(np.max(fuori)) if fuori.size else -1, int(fuori.size)))

    # ================================================================ IL BANCO
    testi = {}
    for nome in FISICA2:
        p = os.path.join(_QUI, nome)
        testi[nome] = io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    cattivi = [n for n, t in testi.items()
               if ("import soliton_simulator" in t or "from soliton_simulator" in t)]
    esito("### il banco v2 non IMPORTA il simulatore", not cattivi,
          "### %d file guardati%s" % (len(testi), (": %s" % cattivi) if cattivi else ""))
    trovati = [(n, c) for n, t in testi.items() for c in CLIP if c in t]
    esito("### NESSUN clip nei file di fisica del banco v2", not trovati,
          "### %d forme cercate in %d file%s"
          % (len(CLIP), len(FISICA2), (": %s" % trovati) if trovati else ""))

    # ================================================================ IL DETERMINISMO
    imp = []
    for _ in range(2):
        pr = subprocess.run([sys.executable, os.path.join(_QUI, "camminata2.py")],
                            cwd=RADICE, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        imp.append((pr.stdout or "").strip())
    esito("### il DETERMINISMO fra DUE PROCESSI: uscita identica",
          len(imp) == 2 and imp[0] == imp[1] and bool(imp[0]),
          "### %d caratteri di uscita, confrontati" % len(imp[0] if imp else ""))

    print("=" * 100)
    print("IL COLLAUDO DEL BANCO v2: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
