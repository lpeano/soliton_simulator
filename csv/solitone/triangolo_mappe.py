# -*- coding: utf-8 -*-
r"""**LE MAPPE DEL TRIANGOLO (T-fase)** *(Luca `2026-11-14` `21:37`, (1): SOLO LETTURA, nessuna corsa; per il video del guardiano)*.

    python csv/solitone/triangolo_mappe.py > doc/referti_l2/mattone/triangolo_fase_mappe.txt     (e doc/referti_l2/mattone/triangolo_fase_mappe.npz)
    python csv/solitone/triangolo_mappe.py --variante sfasati > doc/referti_l2/mattone/triangolo_sfasati_mappe.txt   (Luca 2026-11-15 00:05; senza argomento: fase, come il comando gia' girato)

**Dagli stati salvati di (T-fase)** *(`E:/soliton_simulator/mattone/triangolo_fase_00500` ... `02000`, la corsa a `4944c640`)* **e dallo stato INIZIALE** *(NON salvato dalla corsa: RICOSTRUITO con le righe
dell'incollatura di `mattone_triangolo.corsa`, i francobolli, i vertici, la somma e il prodotto, il campo di Gauss con `A = 0`; nessun tick; dichiarato)*: **tre mappe per stato, `float32`:**
**`rho`** *(la somma su `c` di `|psi_c|^2` per nodo, `mattone.rho_di`)*; **`|phi - phi0|`** *(per nodo, la norma sulle `6` estremita': `sqrt(somma |phi - phi0|^2)`; `phi0 = c(t) F3`, `mattone.vuoto_fresco` al tick
`60000 + k`)*; **`|E|`** *(per nodo, sui `3` archi che partono dal nodo, `sqrt(somma E_a^2)`: mia scelta, dichiarata)*. **Le coordinate dei nodi:** **`m1`, `m2` e la posizione `x, y = m1 A1 + m2 A2`** *(`toro.vettori`, come
i video di G1)*; **i centri dei tre solitoni** *(dalla serie della corsa, `triangolo_fase_serie.npz`, agli stessi tick)*.
"""
import json
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


def main(variante):
    import _presidio
    from solitone import toro as TO
    for m in ("mattone", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    serie = np.load(os.path.join(MT.DIR_REF, "triangolo_%s_serie.npz" % variante))
    frs = [MTR.francobollo(k) for k in MTR.VARIANTI[variante]]
    print("=" * 130)
    print("LE MAPPE DEL TRIANGOLO (T-%s) (Luca 21:37; 00:05 per sfasati; solo lettura): rho, |phi - phi0|, |E| ai tick %s; lo stato 0 RICOSTRUITO (le righe dell'incollatura di mattone_triangolo.corsa)" % (variante, TICK))
    print("=" * 130)
    out = {}
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        st, L, n, righe = Z["st"], Z["L"], Z["n"], Z["righe"]
        A1, A2 = TO.vettori()
        xy = Z["m1"][:, None] * A1[None, :] + Z["m2"][:, None] * A2[None, :]
        out.update(m1=Z["m1"].astype(np.int16), m2=Z["m2"].astype(np.int16), x=xy[:, 0].astype(np.float32), y=xy[:, 1].astype(np.float32), L=np.int16(L))
        # ---------------------------------------------------------------- lo stato 0, ricostruito (le righe di mattone_triangolo.corsa)
        c0 = Z["bordo"]["c0"]
        centri = MTR.posti(c0, frs, L)
        MT.vuoto_fresco(Z, t0)
        phi_F3 = st["phi_h"].copy()
        vuoto = {x: st[x].copy() for x in Z["chiavi"]}
        soli = []
        for fr, c in zip(frs, centri):
            for x in Z["chiavi"]:
                st[x][...] = vuoto[x]
            MT.incolla(Z, fr, c, True)
            soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
        psi, phi = soli[0][0].copy(), soli[0][1].copy()
        for s_ in soli[1:]:
            psi = psi + s_[0]
            phi = phi * (s_[1] / phi_F3)
        st["psi_h"][...] = psi
        st["phi_h"][...] = phi
        C = MT.Campi(Z, "MGU", rho_c, e)
        rho = MT.rho_di(Z)
        C.campo.E[...] = C.gauss(e * (rho - rho.mean()))
        stati = {0: ({x: st[x].copy() for x in Z["chiavi"]}, C.campo.E.copy())}
        print("### lo stato 0 ricostruito: i vertici %s; la massa %.10e (la serie della corsa a k 0: le masse dei pezzi %s)"
              % (centri, float(rho.sum()), ["%.10e" % serie["M_" + q][0] for q in "ABC"]))
        for k in TICK[1:]:
            f = os.path.join(MT.DIR_E, "triangolo_%s_%05d.npz" % (variante, k))
            with np.load(f) as d:
                stati[k] = ({x: d[x].copy() for x in Z["chiavi"]}, d["campo_E"].copy())
                print("### lo stato %d: %s (lo sha di psi_h nel meta %s)" % (k, f, json.loads(str(d["meta"]))["sha"].get("psi_h")))
        for k in TICK:
            dati, E = stati[k]
            Z["metti"](dati)
            rho = MT.rho_di(Z)
            MT.vuoto_fresco(Z, t0 + k)
            phi0 = st["phi_h"].copy()
            Z["metti"](dati)
            dphi = np.sqrt(np.sum(np.abs(st["phi_h"] - phi0).reshape(n * 6, -1) ** 2, axis=1))
            dphi_nodo = np.sqrt(np.sum(dphi[righe] ** 2, axis=1))
            E_nodo = np.sqrt(np.sum(E.reshape(n, 3) ** 2, axis=1))
            j = int(np.nonzero(serie["k"] == k)[0][0])
            cen = np.array([[serie["c1_" + q][j], serie["c2_" + q][j]] for q in "ABC"], dtype=np.float32)
            out["rho_%05d" % k] = rho.astype(np.float32)
            out["dphi_%05d" % k] = dphi_nodo.astype(np.float32)
            out["E_%05d" % k] = E_nodo.astype(np.float32)
            out["centri_%05d" % k] = cen
            print("    k %4d: rho max %.4e, somma %.6e; |phi - phi0| max %.4e; |E| max %.4e; i centri %s" % (k, rho.max(), rho.sum(), dphi_nodo.max(), E_nodo.max(), [list(map(float, c)) for c in cen]))
        Z["metti"]()
    out["tick"] = np.array(TICK, dtype=np.int16)
    f = os.path.join(MT.DIR_REF, "triangolo_%s_mappe.npz" % variante)
    np.savez_compressed(f, **out)
    print("### %s: %.2f MB" % (f, os.path.getsize(f) / 1e6))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(main(a[a.index("--variante") + 1] if "--variante" in a else "fase"))
