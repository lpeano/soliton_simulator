# -*- coding: utf-8 -*-
r"""**`DECISIONE-LINEARE`: IL CONFRONTO FRA `S1` E `S4`, LE DUE FORME CHE RISPETTANO IL CRITERIO DI LUCA.**

> ### ⛔ **Il task history e' `2026-10-22_lineare_s1_s4.md`**: il criterio alla lettera, le previsioni, le letture. ### **Le forme
> SOLO IN MEMORIA** *(`_screening_forme_s3.forma`)*; ### **`leggi.yaml`, il passo e l'impronta non si toccano. NESSUNA FORMA
> SCELTA.**

## LE PARTI, una per corsa *(il riavvio notturno di Luca)*
`--parte controlli` *(`S3` al bit con `594417f6` `R2` e `R1`, l'accoppiamento, la camminata sola)* · `--parte scala` *(`S1`, `S4`, `R2`,
`x 0.1`, lato `32` e `64`, `N dtau 400`, la linearita')* · `--parte materia` *(`x` `0.01`, `0.3`, `1`, `3`)* · `--parte cs` *(`R1`)* ·
`--sintesi`.

Gira con:  python csv/_lineare_s1_s4.py --parte controlli    (e scala, materia, cs; poi --sintesi)
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

EPS = float(np.finfo(float).eps)
FORME = ("S1", "S4")
TEMPO = 400.0                  # N dtau, dal mandato
TAGLIE = ((32, 0.125), (64, 0.0625))
X_MATERIA = (0.01, 0.3, 1.0, 3.0)
X_ACC = (0.01, 0.1, 0.3, 1.0, 3.0)
TOLL_ACC = 1e-8
ASINT = 0.10                   # seconda meta' contro ultimo quarto, al k del massimo, dal mandato
GAMMA_TAGLIE = 0.10            # gamma alle due taglie, dal mandato
CARTELLA = os.path.join(RADICE, "doc", "referti_l2")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def jl(parte):
    return os.path.join(CARTELLA, "lineare_s1_s4_%s.jsonl" % parte)


def salva(parte, r):
    with io.open(jl(parte), "a", encoding="utf-8") as f:
        f.write(json.dumps(r) + "\n")


def corsa(nome_forma, legge, x, lato, dtau, eps_rel, tempo):
    """### Un braccio `R2` o `R1` sul quadrato, con la forma in memoria e la `x` della scena."""
    import _prova_grover as PG
    import _screening_forme_s3 as SF
    import _stabilita_triangoli as ST
    import _triangoli as T
    import _triangoli_r1 as TR
    nome = "%s %s x %g lato %d eps %g N dtau %g" % (legge, nome_forma, x, lato, eps_rel, tempo)
    with SF.forma(nome_forma), PG.variante((), x):
        if legge == "R2":
            b = ST.braccio_proiettato(nome, T.QUADRATO, "Q", eps_rel, tempo, lato, dtau)
        else:
            b = TR.braccio_r1(nome, T.QUADRATO, "Q", eps_rel, tempo, lato, dtau)
    return nome, b


def leggi_braccio(b):
    """### Il massimo della norma, dove, il `k` ripiegato in unita' di `pi`, e l'asintoticita'."""
    g = np.asarray(b["pend"]["meta_norm"])
    q4 = np.asarray(b["pend"]["q4_norm"])
    L = g.shape[0]
    i = tuple(int(a) for a in np.unravel_index(int(np.argmax(g)), g.shape))
    f = [abs(m if m <= L // 2 else m - L) * 2.0 / L for m in i]
    return {"max": float(g.max()), "dove": list(i), "k_pi": sorted(f), "q4": float(q4[i]),
            "asint": abs(float(q4[i]) - float(g[i])) / abs(float(g[i])) if g[i] else float("inf"),
            "minimo": sorted(f) == [0.0, 2.0 / L]}


def riga(nome, b):
    r = leggi_braccio(b)
    print("  %-44s max %.5f a %s (k %s pi); ultimo quarto %.5f (scarto %.3f); uniformita' %.1f ulp; %.0f s"
          % (nome, r["max"], tuple(r["dove"]), ["%.4f" % v for v in r["k_pi"]], r["q4"], r["asint"],
             b["uniformita_ulp"], b["secondi"]))
    sys.stdout.flush()
    return r


def controlli_braccio(nome, b, r):
    import _stabilita_lineare as SL
    esito("%s: la base <= %g ulp" % (nome, SL.SOGLIA_UNIF), b["uniformita_ulp"] <= SL.SOGLIA_UNIF,
          "%.1f ulp" % b["uniformita_ulp"])
    esito("%s: asintotico, seconda meta' contro ultimo quarto entro %g" % (nome, ASINT), r["asint"] <= ASINT,
          "%.3f" % r["asint"])


# =====================================================================================
#   LE PARTI
# =====================================================================================
def parte_controlli():
    import _al_bit_cura_d0 as AB
    import _screening_forme_s3 as SF
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import _triangoli as T
    import _triangoli_r1 as TR
    vecchi = AB.committato()
    for legge in ("R2", "R1"):
        t0 = time.time()
        if legge == "R2":
            b = ST.braccio_proiettato("R2 S3", T.QUADRATO, "Q", SL.EPS_REL, SL.TEMPO_LUNGO)
        else:
            b = TR.braccio_r1("R1 S3", T.QUADRATO, "Q", SL.EPS_REL, SL.TEMPO_LUNGO)
        v = vecchi["%s lato 32" % legge]
        diversi = [c for c in AB.CAMPI if not np.array_equal(np.asarray(b[c]), np.asarray(v[c]))]
        diversi += ["pend." + k for k in v["pend"]
                    if not np.array_equal(np.asarray(b["pend"][k]), np.asarray(v["pend"][k]))]
        if not esito("DEVE RIUSCIRE: S3 %s ridà 594417f6 AL BIT (N dtau 100)" % legge, not diversi,
                     ("10 campi identici, %.0f s" % (time.time() - t0)) if not diversi else ", ".join(diversi)):
            print("### STOP: la forma di oggi non ripete 594417f6")
            return 1
        salva("controlli", {"al_bit": legge, "max": float(np.max(b["pend"]["meta_norm"]))})
    for nome in FORME:
        for x in X_ACC:
            fd, xs = SF.acc_codice(nome, x)
            mano = SF.acc_mano(nome, xs)
            rel = abs(fd - mano) / abs(mano)
            esito("%s x %-5g: rho dalpha/drho, codice contro mano" % (nome, x), rel <= TOLL_ACC,
                  "%.10e contro %.10e, %.2e" % (fd, mano, rel))
            salva("controlli", {"accoppiamento": [nome, x], "codice": fd, "mano": mano})
    ex = SL.c2_esatto_lungo(32, 0.125)
    esito("la camminata sola ESATTA, N dtau 100, <= N*64 ulp", ex["dev"] <= ex["N"] * 64 * EPS, "%.3e" % ex["dev"])
    return 0


def parte_scala():
    import _stabilita_lineare as SL
    for nf in FORME:
        rr = {}
        for lato, dtau in TAGLIE:
            nome, b = corsa(nf, "R2", 0.1, lato, dtau, SL.EPS_REL, TEMPO)
            r = riga(nome, b)
            controlli_braccio(nome, b, r)
            rr[lato] = (b, r)
            salva("scala", {"forma": nf, "lato": lato, "dtau": dtau, "lettura": r,
                            "meta_norm": np.asarray(b["pend"]["meta_norm"]).tolist()})
        # ### la linearita', un braccio per forma: lato 32
        nome2, b2 = corsa(nf, "R2", 0.1, 32, 0.125, SL.EPS_REL_2, TEMPO)
        g1 = np.asarray(rr[32][0]["pend"]["meta_norm"])
        g2 = np.asarray(b2["pend"]["meta_norm"])
        dl = float(np.max(np.abs(g1 - g2)))
        tetto = SL.BANDA_LIN * float(np.max(np.abs(g1)))
        esito("%s: la linearita', 1e-7 contro 1e-6 (lato 32)" % nf, dl <= tetto, "%.3e contro %.3e" % (dl, tetto))
        # ### LA PROVA CHE DECIDE
        k32 = np.asarray(rr[32][1]["k_pi"])
        k64 = np.asarray(rr[64][1]["k_pi"])
        passo = 2.0 / 64
        if np.max(np.abs(k64 - k32)) <= passo + 1e-12:
            v = "(a) FISSO IN ARCHI -> artefatto del reticolo"
        elif np.max(np.abs(k64 - k32 / 2.0)) <= passo + 1e-12:
            v = "(b) FISSO IN UNITA' FISICHE -> una scala fisica"
            if rr[32][1]["minimo"] and rr[64][1]["minimo"]:
                v += "; ### (b*) MA AL k MINIMO DEL TORO A TUTTE E DUE LE TAGLIE: la scala e' quella della SCATOLA"
        else:
            v = "(c) NE' L'UNA NE' L'ALTRA -> NON DECIDIBILE"
        g32, g64 = rr[32][1]["max"], rr[64][1]["max"]
        dg = abs(g64 - g32) / abs(g32)
        print("  ### %s: k lato 32 %s, lato 64 %s (in pi) -> %s" % (nf, k32.tolist(), k64.tolist(), v))
        esito("%s: gamma alle due taglie entro %g nel tempo fisico" % (nf, GAMMA_TAGLIE), dg <= GAMMA_TAGLIE,
              "%.5f contro %.5f, %.3f" % (g32, g64, dg))
        salva("scala", {"prova": nf, "k32": k32.tolist(), "k64": k64.tolist(), "verdetto": v,
                        "g32": g32, "g64": g64, "linearita": dl})
    return 0


def parte_materia():
    import _stabilita_lineare as SL
    for nf in FORME:
        for x in X_MATERIA:
            nome, b = corsa(nf, "R2", x, 32, 0.125, SL.EPS_REL, TEMPO)
            r = riga(nome, b)
            controlli_braccio(nome, b, r)
            salva("materia", {"forma": nf, "x": x, "lettura": r, "nu_s3": b["nu_s3"]})
    return 0


def parte_cs():
    import _al_bit_cura_d0 as AB
    import _stabilita_lineare as SL
    rif = float(np.max(AB.committato()["R1 lato 32"]["pend"]["meta_norm"]))
    for nf in FORME:
        nome, b = corsa(nf, "R1", 0.1, 32, 0.125, SL.EPS_REL, TEMPO)
        r = riga(nome, b)
        controlli_braccio(nome, b, r)
        print("      rapporto con R1 di oggi (norma %.4f): %.4f" % (rif, r["max"] / rif))
        salva("cs", {"forma": nf, "lettura": r, "rif": rif, "rapporto": r["max"] / rif})
    return 0


def sintesi():
    print("### LA SINTESI dalle quattro parti")
    righe = {}
    for parte in ("controlli", "scala", "materia", "cs"):
        p = jl(parte)
        righe[parte] = [json.loads(r) for r in io.open(p, encoding="utf-8")] if os.path.exists(p) else None
        print("  %s: %s" % (parte, "%d righe" % len(righe[parte]) if righe[parte] is not None else "### MANCA"))
    out = {}
    if righe["scala"]:
        for r in righe["scala"]:
            if "prova" in r:
                print("  LA SCALA %s: %s (gamma %.5f a lato 32, %.5f a lato 64)" % (r["prova"], r["verdetto"], r["g32"],
                                                                                  r["g64"]))
        out["scala"] = [r for r in righe["scala"] if "prova" in r]
    if righe["materia"] is not None:
        print("  LA MATERIA:  forma  x      gamma max   dove      k (pi)")
        tab = [(r["forma"], 0.1, r["lettura"]) for r in (righe["scala"] or []) if "lettura" in r and r["lato"] == 32]
        tab += [(r["forma"], r["x"], r["lettura"]) for r in righe["materia"]]
        for f, x, L in sorted(tab, key=lambda t: (t[0], t[1])):
            print("               %-5s  %-5g  %.5f     %-9s %s" % (f, x, L["max"], tuple(L["dove"]), L["k_pi"]))
        out["materia"] = [[f, x, L] for f, x, L in tab]
    if righe["cs"]:
        for r in righe["cs"]:
            print("  CON cs (R1) %s: %.5f a %s, rapporto con oggi %.4f" % (r["forma"], r["lettura"]["max"],
                                                                         tuple(r["lettura"]["dove"]), r["rapporto"]))
        out["cs"] = righe["cs"]
    with io.open(os.path.join(CARTELLA, "lineare_s1_s4.jsonl"), "w", encoding="utf-8") as f:
        f.write(json.dumps(out) + "\n")
    return 0


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    print("=" * 100)
    print("DECISIONE-LINEARE: IL CONFRONTO FRA S1 E S4 (in memoria; nessuna forma scelta) -- %s" % " ".join(argv))
    print("=" * 100)
    print("  il passo: %d pezzi, impronta %s (intatto); il quadrato; base proiettata; la NORMA, seconda meta';"
          " N dtau %g (i controlli a 100)" % (len(CM.ORDINE), CM.IMPRONTA, TEMPO))
    print("-" * 100)
    sys.stdout.flush()
    if "--sintesi" in argv:
        return sintesi()
    parte = argv[argv.index("--parte") + 1]
    io.open(jl(parte), "w", encoding="utf-8").close()
    rc = {"controlli": parte_controlli, "scala": parte_scala, "materia": parte_materia, "cs": parte_cs}[parte]()
    print("=" * 100)
    print("LA PARTE %s: %d su %d controlli   %s" % (parte, OK[0], OK[1], "### TUTTI PASSATI"
                                                  if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return rc or (0 if OK[0] == OK[1] else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
