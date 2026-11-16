# -*- coding: utf-8 -*-
r"""**LE FRECCE DEL FLUSSO NEI TRIANGOLI** *(Luca `2026-11-15` `01:58`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `22.3`)*.

    python csv/solitone/triangolo_flussi.py > doc/referti_l2/mattone/triangolo_flussi.txt     (e doc/referti_l2/mattone/triangolo_flussi.npz)

### **IL FLUSSO E' LA SORGENTE `J_a` DI `_u1_prototipo.avvolto`** *(fuori dal nucleo; la corrente di materia che alimenta il campo U: `J_a = |v0'|^2 - |v0|^2` per arco, la materia che il passo di trasporto
`spostamento_trasporto` sposta lungo l'arco `a`)*, **dichiarata come tale** *(Luca `01:58`)*. **Il nucleo NON definisce un flusso per nodo.**
**Solo lettura:** **per ogni stato salvato di (T-fase) e di (T-sfasati)** *(lo stato `0` ricostruito come in `triangolo_mappe.py`; `500` ... `2000` su E:)* **una COPIA dello stato, `U` dal campo salvato**
*(`scrivi_U`)*, **il `cs` della SCENA** *(lo stato salvato non ha il `cs` del lapse: `N = 1` per il passo, dichiarato)*, **UN `spostamento_trasporto` a frazione `0.5`** *(quella del tick)*; **`J_a` per arco; il vettore per
nodo = la somma su `3` archi che partono dal nodo di `J_a` per il vettore dell'arco** *(`A1`, `A2`, `A1 + A2`: mia scelta, dichiarata)*.
"""
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


def main():
    import _presidio
    import _u1_prototipo as U1
    from solitone import toro as TO
    for m in ("mattone", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    FR = {v: [MTR.francobollo(k) for k in MTR.VARIANTI[v]] for v in ("fase", "sfasati")}     # ### i francobolli PRIMA della scena di S162
    print("=" * 130)
    print("LE FRECCE DEL FLUSSO (Luca 01:58): la sorgente J_a di _u1_prototipo (fuori dal nucleo), un spostamento_trasporto a frazione 0.5 su una COPIA di ogni stato, U dal campo, il cs della scena")
    print("=" * 130)
    out = {}
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        st, L, n, mot = Z["st"], Z["L"], Z["n"], Z["mot"]
        A1, A2 = TO.vettori()
        vett = np.stack([A1, A2, A1 + A2])                    # ### l'arco 3v + a: a1, a2, a1 + a2
        xy = Z["m1"][:, None] * A1[None, :] + Z["m2"][:, None] * A2[None, :]
        out.update(m1=Z["m1"].astype(np.int16), m2=Z["m2"].astype(np.int16), x=xy[:, 0].astype(np.float32), y=xy[:, 1].astype(np.float32), L=np.int16(L))
        sp = mot.operatori["spostamento_trasporto"]
        for v in ("fase", "sfasati"):
            serie = np.load(os.path.join(MT.DIR_REF, "triangolo_%s_serie.npz" % v))
            # ---------------------------------------------------------------- lo stato 0 ricostruito (le righe di mattone_triangolo.corsa)
            centri = MTR.posti(Z["bordo"]["c0"], FR[v], L)
            MT.vuoto_fresco(Z, t0)
            phi_F3 = st["phi_h"].copy()
            vuoto = {x: st[x].copy() for x in Z["chiavi"]}
            soli = []
            for fr, c in zip(FR[v], centri):
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
            stati = {0: ({x: st[x].copy() for x in Z["chiavi"]}, C.campo.A.copy())}
            for k in TICK[1:]:
                with np.load(os.path.join(MT.DIR_E, "triangolo_%s_%05d.npz" % (v, k))) as d:
                    stati[k] = ({x: d[x].copy() for x in Z["chiavi"]}, d["campo_A"].copy())
            print("### (T-%s)" % v)
            for k in TICK:
                dati, A = stati[k]
                Z["metti"](dati)
                C.campo.A[...] = A
                U1.scrivi_U(mot, C.campo)
                m = C.campo.m
                vv = st["psi_h"].reshape(m, 2, 2)
                prima = np.sum(np.abs(vv[:, 0, :]) ** 2, axis=1).copy()
                sp(st, Z["par"], 0.5)                           # ### le righe di avvolto.sp: lo spostamento della materia
                J = np.sum(np.abs(st["psi_h"].reshape(m, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
                Z["metti"]()
                Jn = (J.reshape(n, 3)[:, :, None] * vett[None, :, :]).sum(axis=1)
                j = int(np.nonzero(serie["k"] == k)[0][0])
                cen = np.array([[serie["c1_" + q][j], serie["c2_" + q][j]] for q in "ABC"], dtype=np.float32)
                out["%s_J_%05d" % (v, k)] = J.astype(np.float32)
                out["%s_Jx_%05d" % (v, k)] = Jn[:, 0].astype(np.float32)
                out["%s_Jy_%05d" % (v, k)] = Jn[:, 1].astype(np.float32)
                out["%s_centri_%05d" % (v, k)] = cen
                mod = np.hypot(Jn[:, 0], Jn[:, 1])
                print("    k %4d: somma J_a %+.3e (la materia che lascia le code degli archi; non e' zero per forza); |J| per nodo il massimo %.4e al nodo %d (m1 %d, m2 %d); la somma dei moduli %.4e"
                      % (k, float(J.sum()), float(mod.max()), int(np.argmax(mod)), Z["m1"][int(np.argmax(mod))], Z["m2"][int(np.argmax(mod))], float(mod.sum())))
            Z["metti"]()
    out["tick"] = np.array(TICK, dtype=np.int16)
    f = os.path.join(MT.DIR_REF, "triangolo_flussi.npz")
    np.savez_compressed(f, **out)
    print("### %s: %.2f MB" % (f, os.path.getsize(f) / 1e6))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
