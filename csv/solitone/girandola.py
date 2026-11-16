# -*- coding: utf-8 -*-
r"""**LA GIRANDOLA: IL TRIANGOLO A `120` GRADI GIRA?** *(Luca `2026-11-15` `14:22`, il punto `1`; SOLO LETTURA, le misure del guardiano rifatte)*.

    python csv/solitone/girandola.py > doc/referti_l2/mattone/girandola.txt

**Dalle mappe** *(`triangolo_t120_mappe.npz` e, per (T-fase) col mattone di `L 162`, `triangolo_video_mappe.npz`; ogni `20` tick)*, **attorno al baricentro dei tre centri al tick `0`** *(FISSO)*, **ogni `200` tick:**
- **(a)** **l'orientamento della parte a TRE punte: `arg(somma f e^{3 i theta}) / 3` in gradi, per la materia `rho`, il vuoto `|phi - phi0|` e il campo `|E|`** *(i dischi, miei: `rho` entro `32`, il vuoto e `|E|` entro `45`)*;
- **(b)** **lo stesso per anelli:** **`rho` `8-14`, `14-20`, `20-26`, `26-32`; `|E|` `4-12`, `12-20`, `20-30`, `30-45`** *(la rotazione differenziale)*;
- **(c)** **il peso a tre punte di `|E|`: `|m3| / m0` nell'anello `4-12`.**
**In piu'** *(per la sezione «MISURATO» delle considerazioni, verificati e non ricopiati)*: **la densita' al centro** *(la media di `rho` sul disco di raggio `2` attorno al baricentro dei centri di quel tick)*; **il lato medio per finestra di `500` tick; la dispersione delle masse dei tre pezzi** *(`(max - min) / max`, dalla serie)*.
### **L'angolo e' modulo `120` gradi; la serie si SROTOLA** *(mia: fra due misure si prende il salto piu' corto)*. **I numeri del guardiano** *(scritti prima, Luca `14:22`)* **si stampano accanto.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402

OGNI = 200
DISCHI = {"rho": 32.0, "dphi": 45.0, "E": 45.0}
ANELLI = {"rho": ((8, 14), (14, 20), (20, 26), (26, 32)), "E": ((4, 12), (12, 20), (20, 30), (30, 45))}
GUARDIANO = {"T120": "la materia 30.0 -> 23.7; rho interno 30.1 -> -11.0, esterno 30.0 -> 26.1; il vuoto 30.0 +- 0.2; |E| interno -30.7 -> -46.8, esterno 30.4 -> 25.0; il peso a tre punte di |E| circa 0.25",
             "T-fase (video)": "nessuna rotazione (circa 31.3); il peso a tre punte di |E| da 0.13 a 0.02"}


def srotola(gradi):
    """### Gli angoli modulo `120` con il salto piu' corto fra due misure."""
    out = [gradi[0]]
    for g in gradi[1:]:
        d = (g - out[-1] + 60.0) % 120.0 - 60.0
        out.append(out[-1] + d)
    return out


def main():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "mattone.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA GIRANDOLA (Luca 14:22, punto 1; solo lettura): l'orientamento a tre punte arg(somma f e^{3 i theta}) / 3, in gradi, attorno al baricentro dei centri al tick 0; ogni %d tick" % OGNI)
    print("=" * 130)
    for nome, pref in (("T120", "triangolo_t120"), ("T-fase (video)", "triangolo_video")):
        mp = np.load(os.path.join(MT.DIR_REF, "%s_mappe.npz" % pref))
        s = np.load(os.path.join(MT.DIR_REF, "%s_serie.npz" % pref))
        tk = np.array(mp["tick"])
        m1, m2, L = np.array(mp["m1"], dtype=float), np.array(mp["m2"], dtype=float), int(mp["L"])
        c3 = np.asarray(mp["centri"][0], dtype=float)
        c = (float(c3[:, 0].mean()), float(c3[:, 1].mean()))
        xy = TO.scarti(m1, m2, c[0], c[1], L)[:, :2]
        r = np.hypot(xy[:, 0], xy[:, 1])
        e3 = np.exp(3j * np.arctan2(xy[:, 1], xy[:, 0]))
        sel = [i for i, k in enumerate(tk) if k % OGNI == 0]
        print("### %s: il baricentro dei centri al tick 0 (%.3f, %.3f); i fotogrammi %d (k %d ... %d)" % (nome, c[0], c[1], len(sel), tk[sel[0]], tk[sel[-1]]))
        print("    il guardiano (prima): %s" % GUARDIANO[nome])
        col = {}
        for campo, R in DISCHI.items():
            col["%s (entro %g)" % (campo, R)] = srotola([math.degrees(np.angle(np.sum(np.asarray(mp[campo][i], dtype=float)[r <= R] * e3[r <= R]))) / 3.0 for i in sel])
        for campo, an in ANELLI.items():
            for a, b in an:
                m = (r >= a) & (r < b)
                col["%s %g-%g" % (campo, a, b)] = srotola([math.degrees(np.angle(np.sum(np.asarray(mp[campo][i], dtype=float)[m] * e3[m]))) / 3.0 for i in sel])
        m = (r >= 4) & (r < 12)
        peso = [float(abs(np.sum(np.asarray(mp["E"][i], dtype=float)[m] * e3[m])) / np.sum(np.asarray(mp["E"][i], dtype=float)[m])) for i in sel]
        dens = []
        for i in sel:
            cc = np.asarray(mp["centri"][i], dtype=float)
            dd = np.hypot(*TO.scarti(m1, m2, cc[:, 0].mean(), cc[:, 1].mean(), L).T[:2])
            dens.append(float(np.asarray(mp["rho"][i], dtype=float)[dd <= 2.0].mean()))
        chiavi = list(col)
        print("    %6s %s %12s %14s" % ("k", " ".join("%12s" % x[:12] for x in chiavi), "|m3|/m0 |E|", "rho al centro"))
        for j, i in enumerate(sel):
            print("    %6d %s %12.4f %14.4e" % (tk[i], " ".join("%+12.2f" % col[x][j] for x in chiavi), peso[j], dens[j]))
        print("    (le colonne, per esteso: %s)" % "; ".join(chiavi))
        print("    DA ... A: %s; il peso di |E| da %.4f a %.4f; la densita' al centro da %.4e a %.4e (min %.4e, max %.4e)"
              % ("; ".join("%s %+.2f -> %+.2f" % (x, col[x][0], col[x][-1]) for x in chiavi), peso[0], peso[-1], dens[0], dens[-1], min(dens), max(dens)))
        k = np.array(s["k"], dtype=float)
        lm = (np.array(s["l_AB"]) + np.array(s["l_BC"]) + np.array(s["l_CA"])) / 3.0
        fin = ["%d-%d: %.4f" % (a, a + 500, float(lm[(k > a) & (k <= a + 500)].mean())) for a in range(0, int(k[-1]), 500)]
        M = np.stack([np.array(s["M_" + q]) for q in "ABC"])
        disp = (M.max(axis=0) - M.min(axis=0)) / M.max(axis=0)
        print("    il lato medio da %.4f a %.4f; per finestra di 500: %s; la dispersione delle masse dei pezzi (max - min) / max: al tick 0 %.4f, il massimo %.4f (a k %d), alla fine %.4f"
              % (lm[0], lm[-1], "; ".join(fin), disp[0], disp.max(), int(k[int(disp.argmax())]), disp[-1]))
        print("-" * 130)
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
