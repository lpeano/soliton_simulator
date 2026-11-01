# -*- coding: utf-8 -*-
"""LE FORME DEL LEGAME NEL NUCLEO — **`S1` dalla tabella, `S3` come opzione esplicita, e la rotazione gemella per tutte e due.**

> **Decisione di Luca del `2026-11-01`** *(`16:52`; la decisione (1) delle `01:27`)*: il nucleo usa `S1`, letta dalla tabella
> *(`CAMM-MATERIA-VUOTO`, `parametri.forma`)*; `S3` resta per riprodurre il vecchio.

## CHE COSA PROVA
- ### **la forma del nucleo E' quella della tabella**, e le forme del nucleo SONO gli `ammessi` della tabella;
- ### **`alpha = dN/drho` e `beta = dN/dLambda` per `S1` e per `S3`** *(differenze finite: acbdfb88, la rotazione gemella)*;
- ### **`S1` sono le espressioni di `csv/`** *(`x^2/(1+x^2)`, `x - arctan x - x^3/(1+x^2)`, `Lambda (x - arctan x)`)*, al bit;
- ### **il limite di `S1` a `Lambda = 0`** *(`1`, `-pi/2`, `rho`)*, e ### **`0` dove `rho = 0`**;
- ### **l'opzione esplicita** rimette la forma di prima all'uscita, e ### **una forma fuori dal nucleo ALZA** *(il caso che DEVE fallire)*.

Gira con:  python primo_ordine/_collauda_forme.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import _genera as GE                                          # noqa: E402
import materia_vuoto as MV                                    # noqa: E402

OK = [0, 0]
H = 1e-6
TOLL_FD = 1e-7                  # ### differenze centrate a passo 1e-6: l'errore e' O(h^2) ~ 1e-12 piu' l'arrotondamento ~ eps/h ~ 1e-10


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-78s %s   %s" % (che[:78], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 110)
    print("LE FORME DEL LEGAME NEL NUCLEO -- S1 dalla tabella, S3 opzione esplicita (Luca 2026-11-01 16:52)")
    print("=" * 110)
    leggi, _v, _o = GE.carica()
    voce = [x for x in leggi if x.get("id") == "CAMM-MATERIA-VUOTO"][0]
    pf = voce["parametri"]["forma"]
    esito("la forma del nucleo = il valore della tabella (S1)", MV.FORMA == pf["valore"] == "S1" and MV.ATTIVA == "S1", "%s" % MV.FORMA)
    esito("le forme del nucleo = gli `ammessi` della tabella", sorted(MV.FORME) == sorted(pf["ammessi"]), "%s" % sorted(MV.FORME))
    esito("il generatore della tabella = quello della forma predefinita", voce["generatore"] == pf["ammessi"][pf["valore"]], voce["generatore"])
    for y in (4.0, 0.7):
        for nome in sorted(MV.FORME):
            Nf, af, bf = MV.FORME[nome]
            for x in (0.3, 1.0, 2.5):
                dr = (Nf(x + H, y) - Nf(x - H, y)) / (2 * H)
                dl = (Nf(x, y + H) - Nf(x, y - H)) / (2 * H)
                ea, eb = abs(float(dr) - float(af(x, y))), abs(float(dl) - float(bf(x, y)))
                esito("%s, rho %g Lambda %g: alpha = dN/drho, beta = dN/dLambda (differenze finite)" % (nome, x, y), ea <= TOLL_FD and eb <= TOLL_FD, "%.1e %.1e" % (ea, eb))
    rho = np.array([0.0, 0.2, 1.0, 3.0, 7.5])
    lam = np.array([1.0, 1.0, 0.5, 2.0, 1.5])
    x = rho[1:] / lam[1:]
    esito("S1 = le espressioni di csv/ (alpha, beta, N), al bit, e 0 dove rho = 0",
          np.array_equal(MV.alpha_s1(rho, lam)[1:], x ** 2 / (1.0 + x ** 2)) and np.array_equal(MV.beta_s1(rho, lam)[1:], x - np.arctan(x) - x ** 3 / (1.0 + x ** 2))
          and np.array_equal(MV.N_s1(rho, lam)[1:], lam[1:] * (x - np.arctan(x))) and MV.alpha_s1(rho, lam)[0] == MV.beta_s1(rho, lam)[0] == MV.N_s1(rho, lam)[0] == 0.0, "")
    big = 1e9
    esito("S1 a Lambda = 0: il limite (alpha 1, beta -pi/2, N rho), e a Lambda piccolo ci si avvicina",
          MV.alpha_s1(2.0, 0.0) == 1.0 and MV.beta_s1(2.0, 0.0) == -0.5 * np.pi and MV.N_s1(2.0, 0.0) == 2.0
          and abs(float(MV.alpha_s1(2.0, 2.0 / big)) - 1.0) < 1e-12 and abs(float(MV.beta_s1(2.0, 2.0 / big)) + 0.5 * np.pi) < 1e-6,
          "beta(x = 1e9) %+.9f" % float(MV.beta_s1(2.0, 2.0 / big)))
    with MV.forma_esplicita("S3"):
        dentro = (MV.ATTIVA, MV.alpha is MV.alpha_s3, MV.N is MV.N_s3)
    esito("l'opzione esplicita S3 sceglie S3 e rimette S1 all'uscita", dentro == ("S3", True, True) and MV.ATTIVA == "S1" and MV.alpha is MV.alpha_s1, "%s" % (dentro,))
    p_a, p_b = MV.pezzi(rho, lam)
    esito("`pezzi` (quello che il motore chiede) da' la forma attiva", np.array_equal(p_a, MV.alpha_s1(rho, lam)) and np.array_equal(p_b, MV.beta_s1(rho, lam)), "")
    try:
        MV.scegli("S2")
        alzato = False
    except AssertionError:
        alzato = True
    esito("### DEVE fallire: una forma fuori dal nucleo (S2) NON si sceglie", alzato and MV.ATTIVA == "S1", "")
    print("=" * 110)
    print("IL COLLAUDO DELLE FORME: %d su %d   %s" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 110)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
