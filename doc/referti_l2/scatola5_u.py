# -*- coding: utf-8 -*-
r"""**R-SCATOLA-U, UN CONTO** *(Luca `2026-11-16` `16:17`; la carta `doc/TASK_HISTORY/2026-11-16_scatola5.md`, sez. `4`; nessuna corsa)*.

    python doc/referti_l2/scatola5_u.py > doc/referti_l2/scatola5_u.txt

**Le forze:** `d''` dalla riga «sui tick `250`-`2000`» e `d0` dalla riga «d0 VERA» di tre referti delle coppie *(letti dal file)*.
**La legge di coda:** `|F| = A d^(-n)`: la potenza LONTANA sui punti `51`-`66` *(per `d >= 51`)*, la potenza VICINA sui punti `35`-`51` *(per `d < 51`)*.
**Le copie:** una scena di estensione `d` su un toro `L`: l'immagine piu' vicina del compagno a `L - d`; il rapporto `F(L - d) / F(d)` sotto il `5%`.
**I tori minimi di R-SCATOLA al 5%:** `R_ogg = r_scena + 25` *(il raggio dell'oggetto: meta' della coppia, il raggio circoscritto del triangolo; piu' il raggio del 5% del vuoto del mattone)*; **le TRE clausole** *(la correzione di Luca `16:58`, `porto.regola`)*: **la distanza dal centro al LATO del rombo `L sqrt(3)/4` almeno `max(3 R_ogg, 2 R_ogg + 30)`** *(`R_A = 2 R_ogg`, la fascia `>= 30`)*, `L` intero per eccesso. *(La prima versione usava `L = 6 R_ogg`, col raggio inscritto `L/2`: sbagliato, Luca `17:3x`.)*
**Il mattone da solo** *(Luca)*: **le sei copie si annullano per simmetria** *(nessuna forza netta, solo una marea)*: **il rapporto e' un riferimento CONVENZIONALE, non un blocco.**
"""
import math
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
FILE = [os.path.join(_RADICE, "doc", "referti_l2", "mattone", f) for f in ("coppia_GU_L162.txt", "coppia_GUd50_L162.txt", "coppia_GUd65_L243.txt")]
R5_MATTONE = 25.0
SOGLIA = 0.05


def leggi(f):
    d0 = F = None
    for r in open(f, encoding="utf-8"):
        m = re.search(r"### d0 VERA \(dai semipiani, sullo stato incollato\): ([0-9.]+)", r)
        if m:
            d0 = float(m.group(1))
        m = re.search(r"d'' sui tick 250-2000 ([-0-9.e+]+) \+- ([0-9.e+-]+)", r)
        if m:
            F = (float(m.group(1)), float(m.group(2)))
    assert d0 is not None and F is not None, "il referto %s non ha le due righe" % f
    return d0, F


def main():
    sys.path.insert(0, os.path.join(_RADICE, "csv"))
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("R-SCATOLA-U (Luca 16:17): la forza delle copie periodiche contro la forza che una scena vuole misurare; la soglia %g" % SOGLIA)
    print("=" * 130)
    P = []
    for f in FILE:
        d0, (F, e) = leggi(f)
        P.append((d0, abs(F)))
        print("    %-28s d0 %.6f  d'' %+.6e +- %.1e" % (os.path.basename(f), d0, F, e))
    (d1, f1), (d2, f2), (d3, f3) = P
    n_v = math.log(f1 / f2) / math.log(d2 / d1)
    n_l = math.log(f2 / f3) / math.log(d3 / d2)
    print("### le leggi: la potenza VICINA (%.2f-%.2f) n = %.3f; la potenza LONTANA (%.2f-%.2f) n = %.3f (i tre punti NON stanno su una sola potenza: dichiarato)" % (d1, d2, n_v, d2, d3, n_l))

    def F(d):
        if d >= d2:
            return f3 * (d3 / d) ** n_l
        return f1 * (d1 / d) ** n_v
    print("    la legge alle distanze dei punti: F(%.2f) %.3e (misura %.3e); F(%.2f) %.3e (%.3e); F(%.2f) %.3e (%.3e)" % (d1, F(d1), f1, d2, F(d2), f2, d3, F(d3), f3))
    scene = [("il mattone da solo", 0.0, 0.0, "nessun compagno: l'immagine di se' a L; il riferimento F(%.0f), la forza piu' piccola misurata (dichiarato)" % d3),
             ("la coppia a 30", 30.0, 15.0, "l'immagine del compagno a L - 30"),
             ("la coppia a 40", 40.0, 20.0, "l'immagine del compagno a L - 40"),
             ("il triangolo (lato 40)", 40.0, 40.0 / math.sqrt(3.0), "come una coppia a 40: l'immagine piu' vicina di un vertice a L - 40 (dichiarato)")]
    print("-" * 130)
    print("    %-24s %8s %10s %8s %12s %12s %10s   %s" % ("la scena", "d", "R_ogg", "L min", "F(d)", "F(L - d)", "rapporto", ""))
    for nome, d, rs, nota in scene:
        Rg = rs + R5_MATTONE
        lato_min = max(3.0 * Rg, 2.0 * Rg + 30.0)
        Lm = int(math.ceil(lato_min * 4.0 / math.sqrt(3.0)))
        for L in sorted(set([Lm, 162, 243, 324] + ([186] if d == 0.0 else []))):
            if d == 0.0:
                fd, fc = F(d3), F(float(L))
            else:
                fd, fc = F(d), F(L - d)
            q = fc / fd
            print("    %-24s %8.1f %10.1f %8s %12.3e %12.3e %9.2f%%   %s%s" % (nome, d, Rg, ("L %d" % L) + (" *" if L == Lm else ""), fd, fc, 100 * q, "SOTTO" if q < SOGLIA else "### SOPRA", ("  (" + nota + ")") if L == Lm else ""))
    print("    (* = il toro minimo di R-SCATOLA al 5% per quella scena, con le TRE clausole: la distanza al lato del rombo L sqrt(3)/4 >= max(3 R_ogg, 2 R_ogg + 30))")
    print("    (il mattone da solo: le sei copie si ANNULLANO per simmetria, nessuna forza netta, solo una marea: il rapporto e' un riferimento CONVENZIONALE, non un blocco -- Luca)")
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
