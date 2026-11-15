# -*- coding: utf-8 -*-
r"""**DENTRO IL TRIANGOLO: LE FASI** *(Luca `2026-11-15` `00:58`, TODO `2`; solo lettura; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `21.7`)*.

    python csv/solitone/triangolo_dentro.py > doc/referti_l2/mattone/triangolo_fase_fasi.txt

**Dagli stati di (T-fase)** *(lo stato `0` RICOSTRUITO con le righe dell'incollatura di `mattone_triangolo.corsa`, come `triangolo_mappe.py`; `triangolo_fase_00500` ... `02000` su E:)*: **la FASE di `psi` per OGNI
componente** *(le `12`: le `6` estremita' di un nodo per le `2` dello spinore, nell'ordine di `argsort(nodo)`)* **in `7` punti** *(i tre vertici = i centri dei solitoni della serie della corsa a quel tick; le tre meta'
dei lati; il baricentro dei tre)*: **la fase della SOMMA su un disco di raggio `2`** *(non la media delle fasi)*, **riferita alla fase della stessa componente nel vertice A; il modulo accanto; la componente PIU'
GRANDE** *(la norma su tutto lo stato)*; **il GIRO della fase attorno al centro per ogni componente** *(la somma delle tre differenze fra le meta' dei lati, ridotte in `(-pi, pi]`, in multipli di `2 pi`)*.
### **Il TODO `1`** *(il flusso di materia per nodo con le definizioni del nucleo)*: **il nucleo NON lo da'** *(`flussi_parziali`: gli operatori del passo; `energia_pesata`: i pesi e l'energia)*: **FERMO di quel punto, scritto.**
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
import mattone_triangolo as MTR  # noqa: E402

TICK = (0, 500, 1000, 1500, 2000)
R_DISCO = 2.0


def ridotta(x):
    """### `x` ridotta in `(-pi, pi]`."""
    y = (x + math.pi) % (2.0 * math.pi) - math.pi
    return math.pi if y == -math.pi else y


def main():
    import _presidio
    from solitone import toro as TO
    for m in ("mattone", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    serie = np.load(os.path.join(MT.DIR_REF, "triangolo_fase_serie.npz"))
    frs = [MTR.francobollo(k) for k in MTR.VARIANTI["fase"]]         # ### i francobolli PRIMA della scena di S162
    print("=" * 140)
    print("DENTRO IL TRIANGOLO (T-fase), LE FASI (Luca 00:58, TODO 2; solo lettura): la fase della SOMMA su un disco di raggio %g per componente, riferita al vertice A; il giro attorno al centro" % R_DISCO)
    print("### IL TODO 1 (il flusso per nodo): il nucleo NON lo da' (flussi_parziali: gli operatori del passo; energia_pesata: i pesi e l'energia): FERMO di quel punto")
    print("=" * 140)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        st, L, righe, m1, m2 = Z["st"], Z["L"], Z["righe"], Z["m1"], Z["m2"]
        # ---------------------------------------------------------------- lo stato 0 ricostruito (le righe di mattone_triangolo.corsa)
        centri = MTR.posti(Z["bordo"]["c0"], frs, L)
        MT.vuoto_fresco(Z, t0)
        phi_F3 = st["phi_h"].copy()
        vuoto = {x: st[x].copy() for x in Z["chiavi"]}
        soli = []
        for fr, c in zip(frs, centri):
            for x in Z["chiavi"]:
                st[x][...] = vuoto[x]
            MT.incolla(Z, fr, c, True)
            soli.append(st["psi_h"].copy())
        psi0 = soli[0] + soli[1] + soli[2]
        Z["metti"]()
        stati = {0: psi0}
        for k in TICK[1:]:
            with np.load(os.path.join(MT.DIR_E, "triangolo_fase_%05d.npz" % k)) as d:
                stati[k] = d["psi_h"].copy()
        for k in TICK:
            psi = stati[k][righe].reshape(Z["n"], -1)                 # ### per nodo: le 12 componenti
            nc = psi.shape[1]
            norma = np.sum(np.abs(psi) ** 2, axis=0)
            grande = int(np.argmax(norma))
            j = int(np.nonzero(serie["k"] == k)[0][0])
            V = [(float(serie["c1_" + q][j]), float(serie["c2_" + q][j])) for q in "ABC"]
            mezzi = [((V[a][0] + V[b][0]) / 2.0, (V[a][1] + V[b][1]) / 2.0) for a, b in ((0, 1), (1, 2), (2, 0))]
            centro = (sum(v[0] for v in V) / 3.0, sum(v[1] for v in V) / 3.0)
            punti = [("vertice A", V[0]), ("vertice B", V[1]), ("vertice C", V[2]), ("meta' AB", mezzi[0]), ("meta' BC", mezzi[1]), ("meta' CA", mezzi[2]), ("centro", centro)]
            somme = []
            for _nome, p in punti:
                dd = np.hypot(*TO.scarti(m1, m2, p[0], p[1], L).T[:2])
                somme.append(psi[dd <= R_DISCO].sum(axis=0))
            print("-" * 140)
            print("### k %d: i punti %s; la componente piu' grande %d (la norma %.4e; le norme %s)" % (k, ["%s (%.2f, %.2f)" % (nm, p[0], p[1]) for nm, p in punti], grande, norma[grande],
                  " ".join("%.2e" % x for x in norma)))
            print("    %-10s %s" % ("la comp.", "  ".join("%-17s" % nm for nm, _p in punti) + "  il giro"))
            for i_riga, c in enumerate(list(range(nc)) + [grande]):
                fa = math.atan2(somme[0][c].imag, somme[0][c].real)
                cell = []
                for s in somme:
                    f = ridotta(math.atan2(s[c].imag, s[c].real) - fa)
                    cell.append("%+7.1f %8.2e" % (math.degrees(f), abs(s[c])))
                fm = [math.atan2(somme[3 + i][c].imag, somme[3 + i][c].real) for i in range(3)]
                giro = sum(ridotta(fm[(i + 1) % 3] - fm[i]) for i in range(3)) / (2.0 * math.pi)
                print("    %-10s %s  %+.2f" % (("%d" % c) if i_riga < nc else "%d (la piu' grande)" % c, "  ".join(cell), giro))
        print("    (le celle: la fase in gradi riferita al vertice A, poi il modulo della somma; l'ultima riga: la componente piu' grande, ripetuta)")
    print("=" * 140)
    return 0


if __name__ == "__main__":
    sys.exit(main())
