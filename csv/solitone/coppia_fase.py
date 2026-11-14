# -*- coding: utf-8 -*-
r"""**LA FASE RELATIVA: LA CONTROPROVA B2-`pi`, LA LETTURA ATTRAE/RESPINGE, LA FASE DI (T-sfasati)** *(Luca `2026-11-14` `22:44`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `20`)*.

    python csv/solitone/coppia_fase.py pi --registro coppia-GUpi-L162 > <scratchpad>/coppia_GUpi_L162.txt     (poi doc/referti_l2/mattone/coppia_GUpi_L162.txt)
    python csv/solitone/coppia_fase.py lettura --mondo GU|GUpi > doc/referti_l2/mattone/coppia_<mondo>_lettura.txt
    python csv/solitone/coppia_fase.py fase > doc/referti_l2/mattone/triangolo_fase_relativa.txt            (solo lettura)

### **`pi`** *(la controprova (4))*: **`mattone_coppia_L162.main` COSI' COM'E'** *(e' in uso da B2: non si tocca)* **con IN MEMORIA un mondo `GUpi`** *(i file `coppia_GUpi_L162_*`)* **e `mattone.incolla` che alla SECONDA
incollatura** *(il mattone B)* **usa il francobollo con `psi -> -psi`** *(la fase relativa `pi`)*; **tutto il resto identico a B2.**
### **`lettura`** *((3), l'errore del guardiano n.165)*: **`d''` dalla parabola di `d` sui tick `250`-`2000`** *(`carta_coppia.curvatura`, come B3)*: **negativa oltre `3` errori: ATTRAE; positiva oltre `3`: RESPINGE; dentro:
NIENTE; il confronto con la previsione** *(GU: (a) ATTRAE; GUpi: (b) RESPINGE)*.
### **`fase`** *((c), solo lettura)*: **(i) i francobolli di (T-sfasati)** *(`MGU_08000`, `09000`, `10000`)* **messi sullo STESSO centro: `arg <psi_i, psi_j>` su tutto il francobollo** *(la fase interna relativa; per (T-fase), tre copie, e' `0`
per costruzione: il controllo)*; **(ii) nel triangolo ricostruito all'incollatura** *(le righe di `mattone_triangolo.corsa`)*: **`arg <psi_i, psi_j>` sui nodi dove i due francobolli incollati da soli sono entrambi diversi da
zero** *(la zona di sovrapposizione)*.
"""
import argparse
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

N_ERR = 3.0
FIN = (250, 2000)
PREVISIONE = {"GU": "ATTRAE", "GUpi": "RESPINGE"}


def pi(argv):
    import _presidio
    import mattone_coppia_L162 as MCL
    _presidio.avvia(os.path.join(_QUI, "mattone_coppia_L162.py"))
    _presidio.avvia(__file__)
    MCL.MONDI["GUpi"] = "MGU"
    vero = MT.incolla
    conta = [0]

    def incolla_pi(Z, fr, c, allinea):
        conta[0] += 1
        if conta[0] == 2:                                   # ### il mattone B: psi -> -psi
            fr = dict(fr)
            fr["psi"] = -fr["psi"]
        return vero(Z, fr, c, allinea)
    MT.incolla = incolla_pi
    print("### LA CONTROPROVA B2-pi (Luca 22:44): mattone_coppia_L162.main col mondo GUpi e mattone.incolla col francobollo B a psi -> -psi, SOSTITUITI in memoria")
    try:
        return MCL.main(["--mondo", "GUpi"] + list(argv))
    finally:
        MT.incolla = vero
        print("### le incollature fatte: %d (attese 2: A, poi B girato)" % conta[0])


def lettura(mondo):
    import _presidio
    from solitone import carta_coppia as CC
    _presidio.avvia(__file__)
    s = np.load(os.path.join(MT.DIR_REF, "coppia_%s_L162_serie.npz" % mondo))
    t, d = np.array(s["t"], dtype=float), np.array(s["d"])
    j = (t >= FIN[0]) & (t <= FIN[1])
    a, ea = CC.curvatura(t[j], d[j])
    lett = "ATTRAE" if a < -N_ERR * ea else ("RESPINGE" if a > N_ERR * ea else "NIENTE")
    print("=" * 130)
    print("LA LETTURA DELLA COPPIA %s (Luca 22:44, (3); n.165): d'' sui tick %d-%d %+.6e +- %.1e (%.1f errori); d da %.6f a %.6f" % (mondo, FIN[0], FIN[1], a, ea, abs(a) / ea if ea else float("inf"), d[j][0], d[j][-1]))
    print("  LA LETTURA: %s; LA PREVISIONE (sez. 20, %s): %s -> %s" % (lett, "(a)" if mondo == "GU" else "(b)", PREVISIONE[mondo], "CONFERMATA" if lett == PREVISIONE[mondo] else "### NON CONFERMATA"))
    print("=" * 130)
    return 0


def fase():
    import _presidio
    import mattone_triangolo as MTR
    _presidio.avvia(os.path.join(_QUI, "mattone_triangolo.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA FASE RELATIVA DEI MATTONI DEI TRIANGOLI (Luca 22:44, (c); solo lettura)")
    print("=" * 130)
    for variante in ("fase", "sfasati"):
        frs = [MTR.francobollo(k) for k in MTR.VARIANTI[variante]]
        print("### (T-%s): %s" % (variante, [fr["file"] for fr in frs]))
        # ---------------------------------------------------------------- (i) sullo stesso centro
        chiavi = [dict(((int(a), int(b)), i) for i, (a, b) in enumerate(zip(fr["o1"], fr["o2"]))) for fr in frs]
        for i, j in ((0, 1), (1, 2), (0, 2)):
            comuni = sorted(set(chiavi[i]) & set(chiavi[j]))
            ii = np.array([chiavi[i][x] for x in comuni])
            jj = np.array([chiavi[j][x] for x in comuni])
            z = complex(np.sum(np.conj(frs[i]["psi"][ii]) * frs[j]["psi"][jj]))
            nrm = math.sqrt(float(np.sum(np.abs(frs[i]["psi"][ii]) ** 2)) * float(np.sum(np.abs(frs[j]["psi"][jj]) ** 2)))
            print("    (i)  %s-%s sullo stesso centro (%d nodi): arg <psi_i, psi_j> %+.4f rad (%+.1f gradi); |<psi_i, psi_j>| / (|psi_i| |psi_j|) %.4f"
                  % ("ABC"[i], "ABC"[j], len(comuni), math.atan2(z.imag, z.real), math.degrees(math.atan2(z.imag, z.real)), abs(z) / nrm))
        # ---------------------------------------------------------------- (ii) nel triangolo all'incollatura
        with MT.scena(MT.CORSA_162, MT.T_162) as Z:
            st, L = Z["st"], Z["L"]
            centri = MTR.posti(Z["bordo"]["c0"], frs, L)
            MT.vuoto_fresco(Z, MT.G2.T0)
            vuoto = {x: st[x].copy() for x in Z["chiavi"]}
            soli = []
            for fr, c in zip(frs, centri):
                for x in Z["chiavi"]:
                    st[x][...] = vuoto[x]
                MT.incolla(Z, fr, c, True)
                soli.append(st["psi_h"].copy())
            for i, j in ((0, 1), (1, 2), (0, 2)):
                a, b = soli[i], soli[j]
                zona = (np.abs(a).reshape(len(a), -1).sum(axis=1) > 0) & (np.abs(b).reshape(len(b), -1).sum(axis=1) > 0)
                z = complex(np.sum(np.conj(a[zona]) * b[zona]))
                print("    (ii) %s-%s nel triangolo (i vertici %s, %s; la sovrapposizione %d estremita'): arg <psi_i, psi_j> %+.4f rad (%+.1f gradi); |<psi_i, psi_j>| %.4e"
                      % ("ABC"[i], "ABC"[j], centri[i], centri[j], int(zona.sum()), math.atan2(z.imag, z.real), math.degrees(math.atan2(z.imag, z.real)), abs(z)))
    print("  LA PREVISIONE (c) (sez. 20): la fase relativa di (T-sfasati) fra 0 e pi; il controllo: (T-fase) (i) = 0")
    print("=" * 130)
    return 0


def main(argv):
    if argv and argv[0] == "pi":
        return pi(argv[1:])
    if argv and argv[0] == "fase":
        return fase()
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("lettura",))
    ap.add_argument("--mondo", required=True, choices=sorted(PREVISIONE))
    x = ap.parse_args(argv)
    return lettura(x.mondo)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
