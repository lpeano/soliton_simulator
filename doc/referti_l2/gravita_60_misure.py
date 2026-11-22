# -*- coding: utf-8 -*-
r"""**[M1017-M] LE MISURE DEI DUE MATTONI A DISTANZA 60 E A 39** *(il mandato di Luca [M1017] del `2026-11-22`; la carta `doc/TASK_HISTORY/2026-11-22_gravita_60.md`, sez. `3`; SOLA LETTURA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/gravita_60_misure.py > doc/referti_l2/gravita_60.txt

**Le corse:** F60-on, F60-off *(`CHI/due_corpi`)* e, sola lettura, F-on, F-off a `39`; gli stati `0 ... 3000` ogni `250`, lo sha1 controllato. **(a)** `D(k)` dai baricentri delle due meta' e dal `rho` massimo lisciato *(le righe di `gravita_due_corpi_misure`)*; il fit; `Da_F(60)`, `Da_F(39)` ricalcolato, il rapporto con l'errore propagato; **il caso noto:** gli `a` di F-on e F-off *(i baricentri)* entro l'`1%` da quelli LETTI dal referto `gravita_due_corpi.txt`. **(b)** la congiungente: la striscia `|perp| <= 2.5`, i punti ogni `2` da `-20` a `D + 20` lungo l'asse fra i due baricentri; `rho`, `N - 1`, `|phi - phi0|/|phi0|` *(`phi0(k) = c(t0 + k) F3`)*, la fase del vuoto e della materia meno la media circolare ai due baricentri. **(c)** il disturbo del vuoto al punto di mezzo diviso quello a `r 20` sui lati esterni. **Il film** di F60-on e F60-off con `|phi - phi0|/|phi0|` in piu'.
"""
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import chi_tick as CT  # noqa: E402
import gravita_due_corpi as GD  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402
import girandola_chi_v3 as GC  # noqa: E402

CORSE = (("F60-on", 60), ("F60-off", 60), ("F-on", 39), ("F-off", 39))
KS = tuple(range(0, 3001, 250))
FILM = os.path.join(_QUI, "film")
MEZZA = 2.5          # ### Luca: la striscia larga 5 nodi
PASSO = 2.0          # ### Luca: ogni 2 nodi
FUORI = 20.0         # ### la carta: da 20 prima a 20 dopo (r 20 sui lati esterni)
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def media_circ(a):
    return float(np.angle(np.mean(np.exp(1j * np.asarray(a))))) if len(a) else float("nan")


def rif_39():
    """### gli `a` di F (i baricentri) LETTI dal referto di [M0417] *(a4c7a78d)*."""
    with open(os.path.join(_QUI, "gravita_due_corpi.txt"), encoding="utf-8", errors="replace") as h:
        for r in h:
            m = re.search(r"F, i baricentri\s+a\(on\) ([-+0-9.e]+) \+- ([0-9.e+-]+); a\(off\) ([-+0-9.e]+) \+- ([0-9.e+-]+)", r)
            if m:
                return float(m.group(1)), float(m.group(3))
    raise AssertionError("la riga di F nel referto di [M0417] non c'e': FERMO")


def main():
    import _presidio
    import _u1_prototipo as U1
    from solitone import bordo as BO
    from solitone import toro as TO
    for m in ("gravita_due_corpi.py", "gravita_due_corpi_d.py", "gravita_due_corpi_misure.py", "girandola_chi_v3.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    MT = TC.moduli()[0]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    print("=" * 130)
    print("[M1017-M] I DUE MATTONI IN FASE A DISTANZA 60 E A 39 (la carta sez. 3): gli stati 0 ... 3000 ogni 250; phi0(k) = c(t0 + k) F3, t0 %r" % t0)
    print("=" * 130)
    RIS, C_RIS = {}, {}
    with TC.scena() as Z:
        mot = Z["mot"]
        n, L = mot.inc.n, Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        A1, A2 = TO.vettori()
        A1, A2 = np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]
        vett = np.stack([A1, A2, A1 + A2])
        m1, m2 = np.asarray(Z["m1"], float), np.asarray(Z["m2"], float)
        cam = MT.Campi(Z, "MGU", rho_c, e).campo
        sp = mot.operatori["spostamento_trasporto"]
        cs0 = mot.cs
        for nome, d in CORSE:
            dd = os.path.join(GD.BASE, nome)
            fs = [os.path.join(dd, "stato_%06d.npz" % k) for k in KS]
            if not all(os.path.exists(f + ".sha1") for f in fs):
                print("### %s: gli stati non ci sono tutti (la corsa non e' finita): saltata" % nome)
                continue
            print("-" * 130)
            X0, meta0 = GM.leggi(fs[0])
            V = np.asarray(meta0["centri"], float)
            M = 0.5 * (V[0] + V[1])
            pm = meta0["parametri"]
            dxy = TO.scarti(m1, m2, M[0], M[1], L)[:, :2]
            u = A1 / np.hypot(*A1)
            meta_s = [dxy @ u < 0.0, dxy @ u >= 0.0]
            kappa = float(pm["kappa"])
            print("### %s: d %d, i vertici %s, il punto medio %s; kappa %r, c0 %r, m0 %r (kappa di on %r)" % (nome, d, V.astype(int).tolist(), M.tolist(), kappa, pm["c0"], pm["m0"], pm["kappa_on"]))
            Db, Dm, F, C_k = [], [], {}, []
            for k, f in zip(KS, fs):
                X, _meta = GM.leggi(f)
                rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
                bari = [(dxy[s] * rho[s][:, None]).sum(axis=0) / rho[s].sum() for s in meta_s]
                g = rho.reshape(L, L)
                lis = ((g + sum(np.roll(np.roll(g, a, 0), b, 1) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)))) / 7.0).reshape(-1)
                mass = [dxy[np.nonzero(s)[0][int(np.argmax(lis[s]))]] for s in meta_s]
                D = float(np.hypot(*(bari[1] - bari[0])))
                Db.append(D)
                Dm.append(float(np.hypot(*(mass[1] - mass[0]))))
                # ### (b) la congiungente
                N = np.exp(-kappa * X["chi"])
                phi0 = BO.c_di(t0 + k, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
                ph = X["phi_h"]
                w0 = np.abs(phi0)
                assert np.all(w0 > 0.0), "phi0 ha semiarchi a zero: |phi - phi0|/|phi0| non e' definito: FERMO"
                dphi = np.bincount(nodo, weights=np.abs(ph - phi0) / w0, minlength=n) / np.bincount(nodo, minlength=n)
                fv = np.angle(np.bincount(nodo, weights=(np.conj(phi0) * ph).real, minlength=n) + 1j * np.bincount(nodo, weights=(np.conj(phi0) * ph).imag, minlength=n))
                ev = (bari[1] - bari[0]) / D
                t = (dxy - bari[0]) @ ev
                p = (dxy - bari[0]) @ np.array([-ev[1], ev[0]])
                stri = np.abs(p) <= MEZZA
                pn = GC.fase_dei_nodi(X["psi_h"], nodo)
                comp = int(np.argmax([np.sum(np.abs(pn[stri, c]) ** 2) for c in (0, 1)]))
                fm = np.angle(pn[:, comp])
                nb = [int(np.argmin(np.hypot(*(dxy - b).T))) for b in bari]
                rv, rm = media_circ(fv[nb]), media_circ(fm[nb])
                centri = np.arange(-FUORI, D + FUORI + 1e-9, PASSO)
                righe = []
                for c in centri:
                    s = stri & (np.abs(t - c) <= 0.5 * PASSO)
                    righe.append((c, float(rho[s].mean()), float((N[s] - 1.0).mean()), float(dphi[s].mean()),
                                  media_circ(np.angle(np.exp(1j * (fv[s] - rv)))), media_circ(np.angle(np.exp(1j * (fm[s] - rm)))), int(s.sum())))
                lont = (np.hypot(*(dxy - bari[0]).T) >= 50.0) & (np.hypot(*(dxy - bari[1]).T) >= 50.0)
                i_m = int(np.argmin(np.abs(centri - 0.5 * D)))
                i_e = [0, int(np.argmin(np.abs(centri - (D + FUORI))))]
                cc = (righe[i_m][3], 0.5 * (righe[i_e[0]][3] + righe[i_e[1]][3]), righe[i_m][4], float(np.median(dphi[lont])))
                C_k.append((k, cc))
                print("    k %4d  D %.4f (rho massimo %.4f); la striscia (la componente %d della materia); il vuoto lontano: la mediana di |phi - phi0|/|phi0| %.4e" % (k, D, Dm[-1], comp, cc[3]))
                print("      t       rho          N - 1         |phi-phi0|/|phi0|   la fase del vuoto   la fase della materia   (nodi)")
                for c, r_, nn_, dp, fvv, fmm, cnt in righe:
                    print("      %+6.1f  %.4e  %+.4e  %.4e        %+.5f            %+.5f              (%d)" % (c, r_, nn_, dp, fvv, fmm, cnt))
                print("      (c) il disturbo al mezzo (t %.1f) %.4e; a r 20 sui lati esterni (t %.1f e %.1f) %.4e; il rapporto %.4f; la fase del vuoto al mezzo %+.5f rad" % (
                    centri[i_m], cc[0], centri[i_e[0]], centri[i_e[1]], cc[1], cc[0] / cc[1], cc[2]))
                if nome.startswith("F60"):
                    Z["metti"]({x: X[x] for x in Z["chiavi"]})
                    cam.A[...] = X["campo_A"]
                    mot.cs = float(pm["s"]) * N
                    mot.lambda_c = None
                    CT.fase_a(mot, Z["st"], float(pm["e0"]), N)
                    U1.scrivi_U(mot, cam)
                    mm = cam.m
                    prima = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1).copy()
                    sp(Z["st"], Z["par"], 0.5)
                    J = np.sum(np.abs(Z["st"]["psi_h"].reshape(mm, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
                    Z["metti"]()
                    Jn = (J.reshape(n, 3)[:, :, None] * vett[None, :, :]).sum(axis=1)
                    sfx = "_%06d" % k
                    F["rho" + sfx], F["chi" + sfx], F["dphi" + sfx] = rho.astype(np.float32), X["chi"].astype(np.float32), dphi.astype(np.float32)
                    F["Jx" + sfx], F["Jy" + sfx] = Jn[:, 0].astype(np.float32), Jn[:, 1].astype(np.float32)
            mot.cs = cs0
            mot.lambda_c = None
            fb, fm_ = GM.fit(KS, np.array(Db)), GM.fit(KS, np.array(Dm))
            print("    (a) il fit sui baricentri: D0 %.4f, v %+.4e, a %+.4e +- %.2e (il residuo rms %.3e); sul rho massimo: a %+.4e +- %.2e (il residuo rms %.3e)" % (fb[0], fb[1], fb[2], fb[3], fb[4], fm_[2], fm_[3], fm_[4]))
            rr = [c[1][0] / c[1][1] for c in C_k]
            print("    (c) il rapporto mezzo / r 20 esterno: la media sugli stati %.4f (da %.4f a %.4f); la fase del vuoto al mezzo: la media %+.5f rad (|.| massimo %.5f)" % (
                float(np.mean(rr)), min(rr), max(rr), float(np.mean([c[1][2] for c in C_k])), max(abs(c[1][2]) for c in C_k)))
            RIS[nome] = (fb, fm_)
            C_RIS[nome] = (float(np.mean(rr)), float(np.mean([abs(c[1][2]) for c in C_k])))
            if nome.startswith("F60"):
                F.update(k=np.array(KS, dtype=np.int32), L=np.array(L), m1=m1.astype(np.float32), m2=m2.astype(np.float32), vertici=V.astype(np.int32), corsa=np.array(nome))
                ff = os.path.join(FILM, "gravita_%s.npz" % nome)
                np.savez_compressed(ff, **F)
                print("    il film %s: %.2f MB (sha1 %s)" % (os.path.relpath(ff, _QUI), os.path.getsize(ff) / 1e6, GM.sha1(ff)[:8]))
                assert os.path.getsize(ff) <= 50e6, "sopra i 50 MB: FERMO"
        Z["metti"]()
    print("=" * 130)
    print("IL CASO NOTO DI (a) E IL CONFRONTO")
    print("=" * 130)
    on39, off39 = rif_39()
    if "F-on" in RIS and "F-off" in RIS:
        a_on, a_off = RIS["F-on"][0][2], RIS["F-off"][0][2]
        r_on, r_off = abs(a_on - on39) / abs(on39), abs(a_off - off39) / abs(off39)
        print("  a d = 39 ricalcolati: a(on) %+.6e (il referto %+.4e, lo scarto relativo %.2e); a(off) %+.6e (il referto %+.4e, %.2e)" % (a_on, on39, r_on, a_off, off39, r_off))
        esito("M CASO NOTO: a d = 39 gli a di F-on e F-off (i baricentri) entro l'1% da quelli del referto di [M0417]", r_on <= 0.01 and r_off <= 0.01)
    for i, che in ((0, "i baricentri"), (1, "il rho massimo")):
        da = {}
        for d_, (on, off) in ((60, ("F60-on", "F60-off")), (39, ("F-on", "F-off"))):
            if on in RIS and off in RIS:
                a1, a2 = RIS[on][i], RIS[off][i]
                da[d_] = (a1[2] - a2[2], math.hypot(a1[3], a2[3]))
                print("  d %d, %-15s a(on) %+.4e +- %.2e; a(off) %+.4e +- %.2e; Da_F %+.4e +- %.2e: %s" % (
                    d_, che, a1[2], a1[3], a2[2], a2[3], da[d_][0], da[d_][1], ("ATTIRA" if da[d_][0] < 0 else "SPINGE") + (" (fuori dall'incertezza)" if abs(da[d_][0]) > 2.0 * da[d_][1] else " (DENTRO l'incertezza)")))
        if 60 in da and 39 in da:
            R = da[60][0] / da[39][0]
            sR = abs(R) * math.hypot(da[60][1] / da[60][0], da[39][1] / da[39][0])
            print("  IL RAPPORTO Da_F(60)/Da_F(39), %s: %+.4f +- %.4f  (le previsioni del mandato: (I) ~0.04, fino a ~0.0015; (II) ~0.52)" % (che, R, sR))
        if "F60-off" in RIS and "F-off" in RIS:
            print("  P-60a, %s: |a(F60-off)| / |a(F-off)| = %.4f" % (che, abs(RIS["F60-off"][i][2]) / abs(RIS["F-off"][i][2])))
    for nome in C_RIS:
        print("  (c) %-8s il rapporto mezzo / r 20 esterno (la media sugli stati) %.4f; |la fase del vuoto al mezzo| media %.5f rad" % (nome, C_RIS[nome][0], C_RIS[nome][1]))
    print("-" * 130)
    print("ESITO: %d/%d" % (sum(ok for _c, ok in ESITI), len(ESITI)))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


if __name__ == "__main__":
    sys.exit(main())
