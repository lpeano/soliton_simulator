# -*- coding: utf-8 -*-
r"""**T4-B, (t-b) RILETTO COL PAVIMENTO DELLO SFONDO VERO** *(Luca `2026-11-09` `12:40`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `16.6`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t4b_rilettura.py > doc/referti_l2/u1_t4b_rilettura.txt

**Lo stesso giro di `u1_t4b_sfondo.py` con lo sfondo azzerato** *(deterministico)*. **R-S:** le righe della tabella col pavimento RELATIVO di prima = quelle del referto
`doc/referti_l2/u1_t4b_sfondo.txt`, al carattere. **Poi la soglia rivista** *(dichiarata)*: **il pavimento di (<-) = `1000 eps_macchina x 1.222e-3 / eps`**, quello dello sfondo vero; **i `V` stampati.**
**La lettura:** `b-s` *(fotone e ottica in fase al pavimento a ogni `k`)* o `b-m`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

SCALA_VERA = 1.222e-03         # ### sez. 16.6 (Luca 12:40): la scala dello sfondo vero, dal referto u1_t4b_sfondo.txt
OK = [0, 0]
FALLITE = []
RIGHE = [("<-fase", "fotone"), ("<-fase", "ottica"), ("<-fase", "gauge"), ("<-ampiezza", "fotone"), ("<-ampiezza", "ottica"), ("->", "fotone"), ("->", "ottica")]


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def tabella(T4B, V, EPS3, pav_di):
    """### Le righe della tabella di `u1_t4b_sfondo.main`, col pavimento `pav_di(d, nk, ver)`: `(righe di testo, {chiave: (p o None, V a 1e-4)})`."""
    lne = np.log(np.array(EPS3))
    testo, P = [], {}
    for d in T4B.DIREZ:
        for nk in T4B.N_K:
            pezzi = []
            for (ver, b) in RIGHE:
                y = np.array([V[(d, nk, ver, b, ep)] for ep in EPS3])
                pav = pav_di(d, nk, ver)
                tl = abs(y[0] - y[1]) / y[0] if y[0] > 0 else float("nan")
                if np.any(y <= pav):
                    P[(d, nk, ver, b)] = (None, y[0])
                    pezzi.append("%-21s" % ("pav (V %.1e)" % y[0]))
                else:
                    p = float(np.polyfit(lne, np.log(y), 1)[0])
                    P[(d, nk, ver, b)] = (p, y[0])
                    pezzi.append("%-21s" % ("p %+.3f L %.1e" % (p, tl)))
            testo.append("  %6s %3d | %s" % ("%d,%d" % d, nk, " | ".join(pezzi)))
    return testo, P


def main():
    import _presidio
    import _u1_prototipo as U1
    import _triangoli_forza as TF
    from solitone import u1_t4b as T4B
    from solitone import u1_t4b_fase as T4F
    from solitone import u1_t4b_sfondo as T4S
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_prototipo.py"))
    for m in ("u1_t4b", "u1_t4b_fase", "u1_t4b_sfondo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    estar = U1.E_PROVA[1]
    EPS3 = T4F.EPS3
    print("=" * 130)
    print("T4-B, (t-b) RILETTO (sez. 16.6): lo sfondo azzerato, e* %.10f, eps %s; il pavimento rivisto di (<-) = %g x eps_macchina x %.3e / eps (lo sfondo vero)" % (estar, EPS3, T4S.FATT_PAV, SCALA_VERA))
    print("=" * 130)
    bl, _f, _r = U1.blocchi_campo(T4B.S)
    with TF.conv(T4B.CONV):
        B = T4B.Banco(U1, estar)
        T4S.con_sfondo_azzerato(B, U1)
        p0, _a, _e = B.tick()
        sc_psi = float(np.sqrt(np.sum(np.abs(p0) ** 2)))
        V = T4S.misura(T4B, T4F, U1, bl, B, EPS3)
    em = np.finfo(float).eps

    def vecchio(d, nk, ver):
        if ver.startswith("<-"):
            return T4S.FATT_PAV * em * np.array([sum(V[(d, nk, ver, bb, ep)] for bb in ("fotone", "ottica", "gauge")) for ep in EPS3])
        return T4S.FATT_PAV * em * sc_psi / np.array(EPS3)

    def nuovo(d, nk, ver):
        return T4S.FATT_PAV * em * (SCALA_VERA if ver.startswith("<-") else sc_psi) / np.array(EPS3)
    # ------------------------------------------------------------------ R-S: lo stesso giro
    tv, _Pv = tabella(T4B, V, EPS3, vecchio)
    ref = open(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "doc", "referti_l2", "u1_t4b_sfondo.txt"), "rb").read().decode("utf-8").splitlines()
    i0 = [i for i, r in enumerate(ref) if r.startswith("### lo sfondo AZZERATO")][0]
    rr = [r for r in ref[i0 + 2:i0 + 2 + len(tv)]]
    uguali = sum(a.rstrip() == b.rstrip() for a, b in zip(tv, rr))
    esito("R-S lo stesso giro: le %d righe della tabella col pavimento di prima = quelle del referto u1_t4b_sfondo.txt, al carattere" % len(tv), uguali == len(tv), "%d su %d" % (uguali, len(tv)))
    # ------------------------------------------------------------------ la soglia rivista
    tn, Pn = tabella(T4B, V, EPS3, nuovo)
    print("-" * 130)
    print("### il pavimento RIVISTO (lo sfondo vero), e i V a eps %g di fotone e ottica in fase:" % EPS3[0])
    print("  %6s %3s | %s" % ("d", "n", " | ".join("%-21s" % ("%s %s" % r) for r in RIGHE)))
    for r_ in tn:
        print(r_)
    print("  i V della fase (fotone / ottica / gauge) e il pavimento rivisto a eps %g (%.2e):" % (EPS3[0], nuovo((1, 0), 1, "<-")[0]))
    for d in T4B.DIREZ:
        print("    d %s: %s" % (d, "  ".join("%d:%.1e/%.1e/%.1e" % (nk, V[(d, nk, "<-fase", "fotone", EPS3[0])], V[(d, nk, "<-fase", "ottica", EPS3[0])], V[(d, nk, "<-fase", "gauge", EPS3[0])]) for nk in T4B.N_K)))
    sopra = [k for k, v in Pn.items() if k[2] == "<-fase" and k[3] in ("fotone", "ottica") and v[0] is not None]
    print("  fotone e ottica in fase sopra il pavimento rivisto: %d k su 48%s" % (len(sopra), (": %s" % ", ".join("%s n %d %s p %+.3f" % (k[0], k[1], k[3], Pn[k][0]) for k in sopra)) if sopra else ""))
    print("  LA LETTURA DI (t-b), COL PAVIMENTO RIVISTO: (%s)" % ("b-s: la parte che restava e' dello SFONDO" if not sopra else "b-m: resta: e' della risposta della materia al campo"))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
