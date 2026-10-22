# -*- coding: utf-8 -*-
r"""**LO SCREENING DELLE QUATTRO FORME CANDIDATE DI `S3`** *(`S1`-`S4`, nessuna forma nuova, nessuna scelta)*.

> ### ⛔ **Il task history e' `2026-10-22_screening_forme_s3.md`**: le forme ALLA LETTERA *(da
> `primo_ordine/_deriva_forme_l2.py`)*, l'accoppiamento a mano, le previsioni, le letture. ### **Le forme entrano SOLO IN
> MEMORIA:** `materia_vuoto.pezzi` *(cio' che `materia_vuoto.applica` chiama per `(alpha, beta)`)* ### **si rimpiazza**;
> ### **`leggi.yaml`, il passo e l'impronta non si toccano.**

## LE FORME *(`N = Lambda F(x)`, `x = rho/Lambda`)*
`S1` `F = x - arctan x` · `S2` `F = x ln x` · `S3` `F = x ln(x/(1+x))` *(oggi)* · `S4` la forma chiusa di
`_deriva_forme_l2.F4`, `alpha4`, `beta4`. ### **L'accoppiamento `rho d alpha/d rho = x F''(x)`**, a mano e per differenze finite.

Gira con:  python csv/_screening_forme_s3.py
"""
import contextlib
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

EPS = float(np.finfo(float).eps)
LATO = 32
DTAU = 0.125
FORME = ("S1", "S2", "S3", "S4")
X_BRACCI = (0.1, 1e-4)
X_CONTROLLO = (1e-4, 1e-2, 0.1, 1.0)
H_FD = 2e-5                    # il passo relativo: troncamento ~h^2/3, arrotondamento ~eps|alpha|/(h acc)
TOLL_ACC = 1e-8                # dal mandato
STABILE, POCA = 1e-3, 0.1      # dal mandato
JSONL = os.path.join(RADICE, "doc", "referti_l2", "screening_forme_s3.jsonl")
J_GRADINO2 = os.path.join(RADICE, "doc", "referti_l2", "triangoli_gradino2.jsonl")
J_DILUITA = os.path.join(RADICE, "doc", "referti_l2", "s3_diluita.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


# =====================================================================================
#   LE FORME
# =====================================================================================
def _ab(nome, x):
    """### `(alpha, beta)` della forma a `x = rho/Lambda > 0`."""
    import _deriva_forme_l2 as DF
    if nome == "S1":
        return x ** 2 / (1.0 + x ** 2), x - np.arctan(x) - x ** 3 / (1.0 + x ** 2)
    if nome == "S2":
        return 1.0 + np.log(x), -x
    if nome == "S4":
        return DF.alpha4(x), DF.beta4(x)
    raise AssertionError(nome)


def pezzi_di(nome):
    import materia_vuoto as MV
    if nome == "S3":
        return MV.pezzi                                 # ### la funzione del CODICE, intatta

    def pezzi(rho, lam):
        rho = np.asarray(rho, dtype=float)
        lam = np.asarray(lam, dtype=float)
        al = np.zeros(np.broadcast(rho, lam).shape)
        be = np.zeros(al.shape)
        vivi = rho > 0.0
        if np.any(vivi):
            r = np.broadcast_to(rho, al.shape)[vivi]
            l_ = np.broadcast_to(lam, al.shape)[vivi]
            a, b = _ab(nome, r / l_)
            al[vivi], be[vivi] = a, b
        return al, be
    return pezzi


@contextlib.contextmanager
def forma(nome):
    import materia_vuoto as MV
    vero = MV.pezzi
    MV.pezzi = pezzi_di(nome)
    try:
        yield
    finally:
        MV.pezzi = vero


def acc_mano(nome, x):
    if nome == "S1":
        return 2.0 * x ** 2 / (1.0 + x ** 2) ** 2
    if nome == "S2":
        return 1.0
    if nome == "S3":
        return 1.0 / (1.0 + x) ** 2
    p = 2.0 / np.pi
    return 4.0 * x ** p / (1.0 + x ** p) ** 2


def acc_codice(nome, x):
    """### `rho d alpha/d rho` per differenze finite centrate, dalla `alpha` della forma, sulla scena a `x`."""
    import _prova_grover as PG
    import _stabilita_triangoli as ST
    import _triangoli as T
    with PG.variante((), x):
        _i, mot, st, _p = ST.scena(T.QUADRATO, "Q", LATO, DTAU)
    rho = float(np.mean(mot.densita_materia(st)))
    lam = float(np.mean(mot.densita_vuoto(st)))
    pz = pezzi_di(nome)
    a1 = float(pz(np.array([rho * (1.0 + H_FD)]), np.array([lam]))[0][0])
    a0 = float(pz(np.array([rho * (1.0 - H_FD)]), np.array([lam]))[0][0])
    return rho * (a1 - a0) / (2.0 * rho * H_FD), rho / lam


# =====================================================================================
#   IL PROGRAMMA
# =====================================================================================
def main(argv):
    del argv
    import _al_bit_cura_d0 as AB
    import _presidio
    _presidio.avvia(__file__)
    import _prova_grover as PG
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import _triangoli as T
    import composizione as CM
    print("=" * 100)
    print("LO SCREENING DELLE QUATTRO FORME CANDIDATE DI S3 (in memoria; nessuna forma scelta)")
    print("=" * 100)
    print("  il passo: %d pezzi, impronta %s (intatto); R2: S3 sola, cs spento, lato %d, dtau %g, eps %g, base"
          " proiettata, N dtau %g, la norma, seconda meta'; Q e T (SE); x %s" % (
              len(CM.ORDINE), CM.IMPRONTA, LATO, DTAU, T.EPS_MONETA, SL.TEMPO_LUNGO, X_BRACCI))
    print("  le forme da primo_ordine/_deriva_forme_l2.py; materia_vuoto.pezzi sostituita in memoria; differenze"
          " finite passo %g, tolleranza %g" % (H_FD, TOLL_ACC))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()

    def salva(r):
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(r) + "\n")

    # ------------------------------------------------------------ 1. l'accoppiamento
    print("### 1. L'ACCOPPIAMENTO: dal codice (differenze finite di alpha) contro la mano")
    for nome in FORME:
        for x in X_CONTROLLO:
            fd, xs = acc_codice(nome, x)
            mano = acc_mano(nome, xs)
            rel = abs(fd - mano) / abs(mano)
            esito("%s x %-6g: rho dalpha/drho" % (nome, x), rel <= TOLL_ACC,
                  "codice %.10e  mano %.10e  relativo %.2e" % (fd, mano, rel))
            salva({"accoppiamento": [nome, x], "codice": fd, "mano": mano})
    print("-" * 100)
    # ------------------------------------------------------------ 2. la camminata sola
    print("### 2. LA CAMMINATA SOLA (non dipende dalla forma)")
    ex = SL.c2_esatto_lungo(LATO, DTAU)
    esito("Q: la camminata sola ESATTA, N dtau 100, <= N*64 ulp", ex["dev"] <= ex["N"] * 64 * EPS,
          "%.3e" % ex["dev"])
    ex = ST.esatta(T.TRIANGOLI)
    esito("T: la camminata sola ESATTA, N dtau 100, <= N*64 ulp", ex["dev"] <= ex["N"] * 64 * EPS,
          "%.3e" % ex["dev"])
    print("-" * 100)
    # ------------------------------------------------------------ 3. i bracci
    print("### 3. I BRACCI R2 (S3 prima: i controlli che ripetono la cosa giusta)")
    vq = AB.committato()["R2 lato 32"]
    vt, vd = None, None
    for riga in io.open(J_GRADINO2, encoding="utf-8"):
        w = json.loads(riga)
        if w.get("nome") == "R2 triangoli SE eps 1e-07":
            vt = w
    for riga in io.open(J_DILUITA, encoding="utf-8"):
        w = json.loads(riga)
        if w.get("nome") == "R2 x 0.0001 eps 1e-07":
            vd = w
    G = {}
    for nome in ("S3", "S1", "S2", "S4"):
        for geo, br, gr in (("Q", "Q", T.QUADRATO), ("T", "SE", T.TRIANGOLI)):
            for x in X_BRACCI:
                t0 = time.time()
                with forma(nome), PG.variante((), x):
                    b = ST.braccio_proiettato("R2 %s %s x %g" % (nome, geo, x), gr, br, SL.EPS_REL, SL.TEMPO_LUNGO)
                g = np.asarray(b["pend"]["meta_norm"])
                G[(nome, geo, x)] = g
                i = tuple(int(a) for a in np.unravel_index(int(np.argmax(g)), g.shape))
                print("  %s %s x %-6g: max gamma %.4f a %s; uniformita' %.1f ulp; %.0f s"
                      % (nome, geo, x, float(g.max()), i, b["uniformita_ulp"], time.time() - t0))
                sys.stdout.flush()
                esito("%s %s x %g: la base <= %g ulp" % (nome, geo, x, SL.SOGLIA_UNIF),
                      b["uniformita_ulp"] <= SL.SOGLIA_UNIF, "%.1f ulp" % b["uniformita_ulp"])
                salva({"braccio": [nome, geo, x], "max": float(g.max()), "dove": list(i),
                       "uniformita_ulp": b["uniformita_ulp"], "meta_norm": g.tolist()})
                if nome == "S3":
                    v = {("Q", 0.1): vq, ("T", 0.1): vt, ("Q", 1e-4): vd}.get((geo, x))
                    if v is not None:
                        rif = v["pend"]["meta_norm"] if "pend" in v else v["meta_norm"]
                        bit = bool(np.array_equal(g, np.asarray(rif)))
                        if not esito("DEVE RIUSCIRE: S3 %s x %g ridà il referto committato AL BIT" % (geo, x),
                                     bit, {("Q", 0.1): "594417f6", ("T", 0.1): "bb0ef057",
                                           ("Q", 1e-4): "07083f09"}[(geo, x)]):
                            print("### STOP: la forma di oggi non ripete il referto")
                            return 1
        # ### la linearita', un braccio per forma: Q a x 0.1
        with forma(nome), PG.variante((), 0.1):
            b2 = ST.braccio_proiettato("R2 %s Q x 0.1 eps 1e-6" % nome, T.QUADRATO, "Q", SL.EPS_REL_2,
                                       SL.TEMPO_LUNGO)
        g1, g2 = G[(nome, "Q", 0.1)], np.asarray(b2["pend"]["meta_norm"])
        dl = float(np.max(np.abs(g1 - g2)))
        tetto = SL.BANDA_LIN * max(float(np.max(g1)), float(np.max(np.abs(g1))))
        esito("%s Q x 0.1: la linearita', 1e-7 contro 1e-6" % nome, dl <= tetto, "%.3e contro %.3e" % (dl, tetto))
    print("-" * 100)
    # ------------------------------------------------------------ 4. le letture
    print("### 4. LE LETTURE E LA TABELLA")
    kv, lab, _M, _K, _d = ST.zona(LATO)
    rif = {geo: float(G[("S3", geo, 0.1)].max()) for geo in ("Q", "T")}
    tab = []
    for nome in FORME:
        r = {"forma": nome, "acc_0": {"S1": "-> 0 (x^2)", "S2": "1 (costante)", "S3": "-> 1",
                                      "S4": "-> 0 (x^0.64)"}[nome]}
        for geo in ("Q", "T"):
            for x in X_BRACCI:
                g = G[(nome, geo, x)]
                i = tuple(int(a) for a in np.unravel_index(int(np.argmax(g)), g.shape))
                r["%s_%g" % (geo, x)] = float(g.max())
                r["%s_%g_dove" % (geo, x)] = list(i) + ([lab[i]] if geo == "T" else [])
            r["%s_rapporto" % geo] = r["%s_0.1" % geo] / rif[geo]
            r["%s_stabile" % geo] = r["%s_0.1" % geo] <= STABILE * rif[geo]
            r["%s_poca" % geo] = r["%s_0.0001" % geo] <= POCA * r["%s_0.1" % geo]
        tab.append(r)
    print("  forma  acc. rho->0     gamma Q 0.1  (rapp.)   gamma T 0.1  (rapp.)   Q 1e-4    T 1e-4    stabile Q/T"
          "   stabile a poca materia Q/T")
    for r in tab:
        print("  %-5s  %-14s  %.4f      (%.3f)   %.4f      (%.3f)   %.4f    %.4f    %s/%s          %s/%s" % (
            r["forma"], r["acc_0"], r["Q_0.1"], r["Q_rapporto"], r["T_0.1"], r["T_rapporto"], r["Q_0.0001"],
            r["T_0.0001"], "SI'" if r["Q_stabile"] else "no", "SI'" if r["T_stabile"] else "no",
            "SI'" if r["Q_poca"] else "no", "SI'" if r["T_poca"] else "no"))
        print("         dove: Q 0.1 %s, T 0.1 %s, Q 1e-4 %s, T 1e-4 %s" % (
            r["Q_0.1_dove"], r["T_0.1_dove"], r["Q_0.0001_dove"], r["T_0.0001_dove"]))
    va_zero = {"S1", "S4"}
    poca = {r["forma"] for r in tab if r["Q_poca"] and r["T_poca"]}
    legame = poca == va_zero
    print("  ### IL LEGAME (le forme con accoppiamento -> 0 sono quelle stabili a poca materia): %s"
          " (stabili a poca materia: %s; accoppiamento -> 0: %s)" % ("TIENE" if legame else "NON TIENE",
                                                                     sorted(poca) or "nessuna", sorted(va_zero)))
    salva({"tabella": tab, "legame": bool(legame)})
    print("=" * 100)
    print("LO SCREENING: %d su %d controlli   %s" % (OK[0], OK[1], "### TUTTI PASSATI"
                                                    if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
