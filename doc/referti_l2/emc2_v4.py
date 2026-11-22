# -*- coding: utf-8 -*-
r"""**[M1446-E2] E = m c^2 -- LA V4** *(la risposta di Luca alla carta del torneo: la v_max della BANDA *(dallo spettro 96 x 96, `spettro.npz`)* e quella del SOLITONE *(`0.588 s`: L1 di [M2357], `lorentz_velocita.txt`, «materia, v_max, la velocita' di gruppo massima»)* una accanto all'altra, con la loro provenienza; R_E con TUTTE E DUE *(al posto di `c_m = 0.588 s` scritto a mano, i due valori LETTI)*, piu' `c = s`; il resto la v3 riga per riga)*. **IL TITOLO DELLA V3: E = m c^2 -- LA V3** *(il mandato di Luca [M1631], 1b: gli `E0` del mandato -- i centri dei gap, i bordi, `0`, `1.103`, `1.101` -- con `m*_sol`; `0` e `1.101` *(l'orologio relativo di [M1417]: `-omega_rel` della base, letto da `orologio_relativo.txt`)* in piu' della v2; lo spettro e' quello di `spettro_gap_v3.py` *(96 x 96)*; il resto la v2 riga per riga)*. **IL TITOLO DELLA V2: E = m c^2 -- LA V2: TUTTI GLI ZERI CANDIDATI** *(la versione nuova del mandato di Luca [M1446], S4; la carta `doc/CARTA_E_mc2.md`, sez. `1`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/emc2_v4.py > doc/referti_l2/E_mc2.txt

**Gli `E0`, scritti nella carta prima dei numeri:** (a) i centri di tutti i gap *(da `spettro.npz` della corsia S)*; (b) i bordi della banda della materia *(le due bande piu' alte a `Gamma`, ordinate per valore: il minimo della penultima, il massimo dell'ultima)*; (c) gli zeri `omega0` di V1-V4 *(letti da `orologio_zero.txt`)*. **Per ciascuno:** `Delta = |omega - E0|` sul cerchio, `R_E = Delta/(|m*| c^2)` per `m*_banda` e `m*_sol` *(da `massa_calcio.txt`, se c'e')*, `c_m = 0.588 s` e `c = s`; la materia sopra o sotto.
"""
import hashlib
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402,F401  (i percorsi)
import spettro_gap as SG  # noqa: E402

C = {"c = s": 0.15}                                                            # ### V4: le due v_max si aggiungono LETTE in main


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "spettro_gap.py"))
    _presidio.avvia(os.path.join(_QUI, "emc2_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "emc2_v3.py"))
    _presidio.avvia(__file__)
    z = np.load(SG.FUORI)
    print("=" * 130)
    print("[M1446-E] E = m c^2, TUTTI GLI ZERI CANDIDATI (la carta sez. 1): lo spettro %s (sha1 %s)" % (SG.FUORI, sha1(SG.FUORI)[:8]))
    print("=" * 130)
    w, d2 = float(z["omega"]), float(z["d2"][0])
    lv = open(os.path.join(_QUI, "lorentz_velocita.txt"), encoding="utf-8").read()
    vs = float(re.search(r"vuoto \(cs = s = 0\.1500\)\s+([0-9.]+)", lv).group(1))
    vb = float(z["vmax"])
    print("### LE DUE v_max, una accanto all'altra: la BANDA %.7f = %.5f s (lo spettro 96 x 96 col raffinamento: il massimo di |dE/dk| della risposta lineare di UN tick sul vuoto della scena di chi, Hellmann-Feynman; spettro_gap_v2.txt); il SOLITONE %.7f = %.5f s (L1 di [M2357], lorentz_velocita.txt sha1 %s: la riga \"materia\" del vuoto cs = s, «v_max, la velocita' di gruppo massima» dai json della materia); lo scarto %+.2f%%" % (
        vb, vb / 0.15, vs, vs / 0.15, sha1(os.path.join(_QUI, "lorentz_velocita.txt"))[:8], 100.0 * (vb / vs - 1.0)))
    C["c = v_banda (%.4f s)" % (vb / 0.15)] = vb
    C["c = v_solitone (%.4f s)" % (vs / 0.15)] = vs
    Es = np.sort(z["E"], axis=1)
    i0 = 0                                                      # ### il punto k = 0 della griglia (i = j = 0)
    bordi = (float(Es[:, 10].min()), float(Es[:, 11].max()))
    print("### la banda della materia (le due piu' alte a Gamma: %+.7f, %+.7f): i bordi %+.7f e %+.7f" % (Es[i0, 10], Es[i0, 11], bordi[0], bordi[1]))
    E0 = [("il centro del gap da %+.4f a %+.4f" % (a, b), float(c)) for a, b, _w, c in z["gap"]]
    E0 += [("il bordo basso della banda della materia", bordi[0]), ("il bordo alto della banda della materia", bordi[1])]
    oz = open(os.path.join(_QUI, "orologio_zero.txt"), encoding="utf-8").read()
    print("### orologio_zero.txt (sha1 %s)" % sha1(os.path.join(_QUI, "orologio_zero.txt"))[:8])
    for m in re.finditer(r"^\s+(V[1-4]): d omega/dN [-+0-9.]+(?: \(RICAVATO: V2 - V3\))?; LO ZERO omega0 = omega\(1\) - d omega/dN = ([-+0-9.]+)", oz, re.M):
        E0.append(("lo zero di %s (orologio_zero)" % m.group(1), float(m.group(2))))
    E0.append(("lo zero simmetrico 0", 0.0))
    rel = open(os.path.join(_QUI, "orologio_relativo.txt"), encoding="utf-8").read()
    mr = re.search(r"LA BASE \(d 50 e d 66\): omega_rel ([-+0-9.e]+)", rel)
    E0.append(("omega_psi - omega_phi locale della base (orologio_relativo, -omega_rel)", -float(mr.group(1))))
    ms = {"m*_banda": 1.0 / d2}
    f = os.path.join(_QUI, "massa_calcio.txt")
    if os.path.exists(f):
        mm = re.search(r"m\*_sol: .*; la media ([-+0-9.]+)", open(f, encoding="utf-8").read())
        if mm:
            ms["m*_sol"] = float(mm.group(1))
    print("### omega(N1) %.10f; %s" % (w, ", ".join("%s %+.4f" % (k, v) for k, v in ms.items())))
    for nome, E in E0:
        dd = (w - E + np.pi) % (2 * np.pi) - np.pi
        righe = []
        for mn, mv in ms.items():
            for cn, c in C.items():
                RE = abs(dd) / (abs(mv) * c * c)
                righe.append("%s, %s: R_E %.4f%s" % (mn, cn, RE, " VALE" if 0.9 < RE < 1.1 else ""))
        print("  E0 %+.6f (%s): Delta %.6f, la materia %s (%s); %s" % (E, nome, abs(dd), "SOTTO" if dd < 0 else "SOPRA", "particella" if dd < 0 else "lacuna", "; ".join(righe)))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
