# -*- coding: utf-8 -*-
r"""**LA MATERIA DILUITA: `R2` SUL QUADRATO A `x = 1e-3` E `1e-4`** *(la banda con pochissima materia)*.

> ### ⛔ **Il task history e' `2026-10-22_s3_due_misure.md`** *(sez. `1.1` e `1.3`)*. ### **Una misura: nessun file
> del nucleo si tocca.** `R2` con `_stabilita_lineare.braccio_proiettato`, ### **cambiando SOLO `x` della scena**;
> ### **`x` `1e-2`, `0.1`, `1` si RILEGGONO da `doc/referti_l2/d0_risonanza_bis.jsonl`**, non si rifanno.

## I CONTROLLI
- ### **DEVE RIUSCIRE:** `nu_S3` stampato *(`Lambda^2/(rho+Lambda)^2` del braccio)* ### **uguale a `rho d alpha/d
  rho` per differenze finite DALLA funzione `materia_vuoto.alpha` del codice**, entro `1e-8` relativo, a ogni `x`.
  ### **Se no, la lettura del guardiano e' sbagliata, e lo si scrive.**
- ### **la linearita'** `1e-7` contro `1e-6` a `x 1e-4`; ### **la base** `<= 1e3` ulp; ### **la camminata sola esatta.**

## LE LETTURE *(sul massimo della banda, `m` da `h/4` a `3h/4` lungo `(m, 0)`)*
### **DILUITA INSTABILE** se `gamma(1e-4) >= 0.5 gamma(0.1)`; ### **SI SPEGNE** se `<= 0.1 gamma(0.1)`; ###
**INTERMEDIO** altrimenti.

Gira con:  python csv/_s3_diluita.py
"""
import io
import json
import os
import sys

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
X_NUOVI = (1e-3, 1e-4)
X_RILETTI = ("0.01", "0.1", "1.0")
H_FD = 1e-5                    # il passo relativo delle differenze finite
TOLL_NU = 1e-8                 # dal mandato
INSTABILE, SPENTA = 0.5, 0.1   # le soglie della lettura, dal mandato
J_BIS = os.path.join(RADICE, "doc", "referti_l2", "d0_risonanza_bis.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "s3_diluita.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-78s %s   %s" % (che[:78], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def nu_fd(x):
    """### `rho d alpha/d rho` per differenze finite centrate, DA `materia_vuoto.alpha`, sulla scena a `x`."""
    import _stabilita_lineare as SL
    import materia_vuoto as MV
    _i, mot, st, _p = SL.scena(LATO, DTAU, x)
    rho = float(np.mean(mot.densita_materia(st)))
    lam = float(np.mean(mot.densita_vuoto(st)))
    a1 = float(MV.alpha(rho * (1.0 + H_FD), lam))
    a0 = float(MV.alpha(rho * (1.0 - H_FD), lam))
    return rho * (a1 - a0) / (2.0 * rho * H_FD), rho, lam


def banda(g):
    """### Il massimo lungo `(m, 0)` per `m` da `h/4` a `3h/4`, e dove."""
    h = LATO // 2
    ms = list(range(h // 4, 3 * h // 4 + 1))
    v = [float(g[m, 0]) for m in ms]
    i = int(np.argmax(v))
    return v[i], ms[i]


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _stabilita_lineare as SL
    import composizione as CM
    print("=" * 100)
    print("LA MATERIA DILUITA: R2 SUL QUADRATO A x = 1e-3 E 1e-4")
    print("=" * 100)
    print("  R2: S3 sola, cs spento; lato %d, dtau %g; base proiettata; N dtau %g; la pendenza della"
          " NORMA sulla seconda meta'; il passo %d pezzi, impronta %s" % (LATO, DTAU, SL.TEMPO_LUNGO,
                                                                        len(CM.ORDINE), CM.IMPRONTA))
    print("  la banda: m da %d a %d lungo (m, 0); differenze finite passo relativo %g, tolleranza %g"
          % (LATO // 8, 3 * LATO // 8, H_FD, TOLL_NU))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    bis = json.loads(io.open(J_BIS, encoding="utf-8").readline())
    righe = []
    # ------------------------------------------------------------ i riletti
    print("### 1. x RILETTI da d0_risonanza_bis")
    for xs in X_RILETTI:
        fd, rho, lam = nu_fd(float(xs))
        nu = float(bis["nu"][xs])
        rel = abs(fd - nu) / nu
        esito("x %s: nu_S3 (d0_risonanza_bis) = rho dalpha/drho per differenze finite" % xs,
              rel <= TOLL_NU, "%.10f contro %.10f, relativo %.2e" % (nu, fd, rel))
        a = np.asarray(bis["gamma"][xs]["(m,0)"])
        ms = list(range(LATO // 8, 3 * LATO // 8 + 1))
        v = [float(a[m]) for m in ms]
        i = int(np.argmax(v))
        righe.append({"x": float(xs), "nu": nu, "nu_fd": fd, "banda": v[i], "m": ms[i], "fonte": "d0_risonanza_bis"})
    print("-" * 100)
    # ------------------------------------------------------------ i nuovi
    print("### 2. x NUOVI")
    ex = SL.c2_esatto_lungo(LATO, DTAU)
    tetto = ex["N"] * SL.ULP_C2 * EPS
    esito("la camminata sola ESATTA, N dtau 100: <= N*64 ulp", ex["dev"] <= tetto,
          "%.3e contro %.3e" % (ex["dev"], tetto))
    bb = {}
    for x, eps_rel in ((1e-3, SL.EPS_REL), (1e-4, SL.EPS_REL), (1e-4, SL.EPS_REL_2)):
        nome = "R2 x %g eps %g" % (x, eps_rel)
        b = SL.braccio_proiettato(nome, LATO, DTAU, x, False, (), eps_rel, SL.TEMPO_LUNGO)
        print("  %-24s rho_m %.6e  Lambda_m %.6f  nu_S3 %.10f  uniformita' %.1f ulp  %.0f s  %s"
              % (nome, b["rho_m"], b["lambda_m"], b["nu_s3"], b["uniformita_ulp"], b["secondi"],
                 b["fine"]))
        sys.stdout.flush()
        if b["fine"] != "N":
            print("### STOP: %s" % b["fine"])
            return 1
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps({"nome": nome, "x": x, "eps_rel": eps_rel, "nu_s3": b["nu_s3"],
                                "uniformita_ulp": b["uniformita_ulp"],
                                "meta_norm": np.asarray(b["pend"]["meta_norm"]).tolist(),
                                "meta_eig": np.asarray(b["pend"]["meta_eig"]).tolist()}) + "\n")
        bb[(x, eps_rel)] = b
    for x in X_NUOVI:
        b = bb[(x, SL.EPS_REL)]
        fd, rho, lam = nu_fd(x)
        rel = abs(fd - b["nu_s3"]) / b["nu_s3"]
        esito("x %g: nu_S3 stampato = rho dalpha/drho per differenze finite da alpha del codice" % x,
              rel <= TOLL_NU, "%.10f contro %.10f, relativo %.2e" % (b["nu_s3"], fd, rel))
        esito("x %g: la base <= %g ulp" % (x, SL.SOGLIA_UNIF), b["uniformita_ulp"] <= SL.SOGLIA_UNIF,
              "%.1f ulp" % b["uniformita_ulp"])
        g = np.asarray(b["pend"]["meta_norm"])
        v, m = banda(g)
        righe.append({"x": x, "nu": b["nu_s3"], "nu_fd": fd, "banda": v, "m": m,
                      "max_tutto": float(g.max()), "fonte": "questa corsa"})
    g1 = np.asarray(bb[(1e-4, SL.EPS_REL)]["pend"]["meta_norm"])
    g2 = np.asarray(bb[(1e-4, SL.EPS_REL_2)]["pend"]["meta_norm"])
    dl = float(np.max(np.abs(g1 - g2)))
    esito("la linearita' a x 1e-4, 1e-7 contro 1e-6", dl <= SL.BANDA_LIN * float(np.max(g1)),
          "%.3e contro %.3e" % (dl, SL.BANDA_LIN * float(np.max(g1))))
    print("-" * 100)
    # ------------------------------------------------------------ la tabella e la lettura
    print("### 3. LA TABELLA E LA LETTURA")
    righe.sort(key=lambda r: r["x"])
    print("     x        nu_S3          gamma della banda   m (lungo (m,0))   fonte")
    for r in righe:
        print("     %-8g %.10f   %.4f              %2d                %s"
              % (r["x"], r["nu"], r["banda"], r["m"], r["fonte"]))
    rif = [r for r in righe if r["x"] == 0.1][0]["banda"]
    g4 = [r for r in righe if r["x"] == 1e-4][0]["banda"]
    q = g4 / rif
    if q >= INSTABILE:
        lettura = "DILUITA INSTABILE"
    elif q <= SPENTA:
        lettura = "SI SPEGNE"
    else:
        lettura = "INTERMEDIO"
    print("  ### LA LETTURA: gamma(1e-4) / gamma(0.1) = %.4f / %.4f = %.4f -> %s"
          " (soglie: >= %g instabile, <= %g si spegne)" % (g4, rif, q, lettura, INSTABILE, SPENTA))
    with io.open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps({"tabella": righe, "rapporto": q, "lettura": lettura}) + "\n")
    print("=" * 100)
    print("LA MATERIA DILUITA: %d su %d controlli   %s" % (OK[0], OK[1], "### TUTTI PASSATI"
                                                          if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
