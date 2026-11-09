# -*- coding: utf-8 -*-
r"""**P1, LA PROVENIENZA DEL LIMITE DI VELOCITA' DELLA MATERIA** *(Luca `2026-11-09` `13:16`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `19`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_p1.py > doc/referti_l2/u1_p1.txt

**`v_b/s`** *(le righe di `_u1_secondo.vb_di`, con `eps` come argomento: il coefficiente di `k^2` nel fit `omega^2 - omega0^2 = v_b^2 k^2 + b k^4` sul ramo lungo della coppia a `K`)*
**e `v_max/s`** *(`_triangoli_forza.v_max(matrice_L(eps, s))`)* **a `eps 0` e `0.5` (la moneta della tabella), alle `s` di `_u1_secondo` e a `s 0.15`** *(la corsa)*; **e la dipendenza dallo zero: lo spostamento `+- pi s / 2` applicato ai livelli** *(la cura della sez. `19.1`)*.
**I DEVE:** `P1-R` *(a `eps 0`, `s 0.05`: `0.784994` di `7daa8840` entro `1e-6`)*; `P1-F` *(DEVE FALLIRE: lo stesso contro il valore della VARIANTE, `0.99916463`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

EPS_P1 = (0.0, 0.5)            # ### Luca 13:16: eps 0 (u1_secondo) e la moneta della tabella
S_CORSA = 0.15                 # ### la corsa
RIF_005 = 0.784994             # ### doc/referti_l2/u1_secondo.txt: a s 0.05, i due rami (7daa8840)
VARIANTE_005 = 0.99916463      # ### doc/referti_l2/u1_terzo.txt: la variante theta = s/x a s 0.05, eps 0
TOLL = 1e-6
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def vb(eps, s):
    """### Le righe di `_u1_secondo.vb_di`, con `eps`."""
    import _triangoli_fattore as F
    import _triangoli_forza as TF
    import _u1_secondo as U2
    bl = TF.blocchi(eps, s)
    out = []
    for b in TF.coppia_K(eps, s):
        qq, ww = F.ramo_lungo(bl, b["Q"], b["w"], U2.KMAX3 * math.sqrt(3.0) / 2.0, U2.NK3)
        k = qq * 2.0 / math.sqrt(3.0)
        y = ww ** 2 - b["w"] ** 2
        X = np.stack([k ** 2, k ** 4], axis=1)
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        # ### la cura (sez. 19.1): la dipendenza dallo ZERO, lo spostamento applicato ai livelli gia' trovati: (omega + z)^2 - (omega0 + z)^2, z = +- pi s / 2
        sp = []
        for z in (math.pi * s / 2.0, -math.pi * s / 2.0):
            cz, *_ = np.linalg.lstsq(X, (ww + z) ** 2 - (b["w"] + z) ** 2, rcond=None)
            sp.append(float(math.sqrt(cz[0])) if cz[0] > 0 else float("nan"))
        out.append((float(math.sqrt(c[0])) if c[0] > 0 else float("nan"), float(b["w"]), sp))
    vm = TF.v_max(TF.matrice_L(eps, s))[0]
    return out, float(vm)


def main():
    import _presidio
    import _triangoli_forza as TF
    import _u1_secondo as U2
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_secondo.py"))
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_triangoli_forza.py"))
    _presidio.avvia(__file__)
    SS = (0.05,) + tuple(U2.S3) + (S_CORSA,)
    print("=" * 130)
    print("P1, LA PROVENIENZA DEL LIMITE DI VELOCITA' DELLA MATERIA (sez. 19): eps %s; s %s; KMAX3 %g NK3 %d (come _u1_secondo); le convenzioni: nessuna (come vb_di), simm, oggi" % (EPS_P1, SS, U2.KMAX3, U2.NK3))
    print("=" * 130)
    ris = {}
    for cnome in ("come vb_di",):      # ### la cura (sez. 19.1): simm fa alzare coppia_K, oggi e' nullcontext (= come vb_di)
        for eps in EPS_P1:
            for s in SS:
                r = vb(eps, s)
                ris[(cnome, eps, s)] = r
                print("  %-10s eps %.1f s %-6g: v_b/s %s (omega0/s %s) | lo zero spostato di +pi s/2: %s, di -pi s/2: %s | v_max/s %.8f" % (
                    cnome, eps, s, " ".join("%.8f" % (v / s) for v, _w, _z in r[0]), " ".join("%+.6f" % (w / s) for _v, w, _z in r[0]),
                    " ".join("%.8f" % (z[0] / s) for _v, _w, z in r[0]), " ".join("%.8f" % (z[1] / s) for _v, _w, z in r[0]), r[1] / s))
                sys.stdout.flush()
    print("-" * 130)
    for cnome in ("come vb_di",):
        for eps in EPS_P1:
            ss = np.array(U2.S3)
            for nome, ys in (("vb0", [ris[(cnome, eps, s)][0][0][0] / s for s in U2.S3]), ("vmax", [ris[(cnome, eps, s)][1] / s for s in U2.S3])):
                p = np.polyfit(ss, np.array(ys), 2)
                print("  il limite a s -> 0 (%-10s eps %.1f) %-4s: f0 %.10f (contro pi/4 %+.3e)" % (cnome, eps, nome, p[2], p[2] - math.pi / 4))
    r005 = ris[("come vb_di", 0.0, 0.05)][0]
    d = max(abs(v / 0.05 - RIF_005) for v, _w, _z in r005)
    esito("P1-R a eps 0, s 0.05 (come vb_di): v_b/s = %.6f di 7daa8840 entro %g, i due rami" % (RIF_005, TOLL), d <= TOLL, "%.1e" % d)
    dv = max(abs(v / 0.05 - VARIANTE_005) for v, _w, _z in r005)
    esito("P1-F lo stesso contro il valore della VARIANTE theta = s/x (%.8f)" % VARIANTE_005, dv <= TOLL, "%.1e" % dv, deve=False)
    rr = ris[("come vb_di", 0.5, S_CORSA)]
    print("  STAMPA il c della materia nel regime delle corse (eps 0.5, s %g): v_b/s %s; con lo zero spostato %s e %s; v_max/s %.6f" % (
        S_CORSA, " ".join("%.6f" % (v / S_CORSA) for v, _w, _z in rr[0]), " ".join("%.6f" % (z[0] / S_CORSA) for _v, _w, z in rr[0]), " ".join("%.6f" % (z[1] / S_CORSA) for _v, _w, z in rr[0]), rr[1] / S_CORSA))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
