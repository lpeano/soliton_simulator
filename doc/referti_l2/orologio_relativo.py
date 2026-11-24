# -*- coding: utf-8 -*-
r"""**[M1417-R] L'OROLOGIO RELATIVO AL VUOTO: omega_rel = omega_phi(locale) - omega_psi** *(la decisione di Luca [M1417]; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `7`; SOLA LETTURA; la lettura e' POST-HOC, dichiarato da Luca)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/orologio_relativo.py > doc/referti_l2/orologio_relativo.txt

**`omega_phi = omega_F3 + omega_v`:** `omega_F3` il ritmo del vuoto indisturbato dalla tabella della scena *(`-arg c(t+1)/c(t)`, tick per tick)*; `omega_v = -wrap(d theta_v)/dk`, `theta_v = arg somma w conj(phi0) phi` *(il ritmo lento: nessuna ambiguita')*; **locale** col peso `rho` entro `r 15` da ciascun mattone, **lontano** col peso `1` dove `r > 40` da tutti e due. **`omega_psi`** come `pound_rebka_GU.py`. **K1** su N1; **K2** il vuoto lontano uguale fra le coppie entro `1e-5`; **K3** il segno di `Delta omega_rel` della coppia che si attrae.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import girandola_chi_v3 as GC  # noqa: E402
import orologio_mattone as OM  # noqa: E402
import pound_rebka_GU as PR  # noqa: E402

R_LOC, R_LONTANO = 15.0, 40.0           # ### Luca: entro r 15; il vuoto lontano r > 40
TOLL_K2 = 1e-5                          # ### Luca: K2
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def arg_c(Z, t1, t2):
    """### la fase di c(t) srotolata tick per tick da t1 a t2 (gli estremi compresi)."""
    from solitone import bordo as BO
    c = np.array([complex(BO.c_di(t, Z["tab_c"], Z["K"], Z["omega"])) for t in range(t1, t2 + 1)])
    return np.unwrap(np.angle(c))


def fasi(Z, psi_h, phi_h, t, nodo, L, centri=None):
    """### per i due mattoni (o il solo, con `centri`): la fase di psi (come pound_rebka), theta_v locale, e theta_v lontano."""
    from solitone import bordo as BO
    from solitone import toro as TO
    n = L * L
    rho = np.bincount(nodo, weights=np.sum(np.abs(psi_h) ** 2, axis=1), minlength=n)
    v = np.arange(n)
    m1, m2 = v // L, v % L
    phi0 = complex(BO.c_di(t, Z["tab_c"], Z["K"], Z["omega"])) * Z["phi_v"]
    zz = np.conj(phi0) * phi_h
    zn = np.bincount(nodo, weights=zz.real, minlength=n) + 1j * np.bincount(nodo, weights=zz.imag, minlength=n)
    pn = GC.fase_dei_nodi(psi_h, nodo)
    if centri is None:
        cg = TO.centro(rho, m1, m2, L)[:2]
        dxy = TO.scarti(m1, m2, cg[0], cg[1], L)[:, :2]
        A1 = np.asarray(TO.vettori()[0], float)[:2]
        xs = dxy @ (A1 / np.hypot(*A1))
        bb = [(dxy[s] * rho[s][:, None]).sum(axis=0) / rho[s].sum() for s in (xs < 0.0, xs >= 0.0)]
    else:
        dxy = TO.scarti(m1, m2, centri[0][0], centri[0][1], L)[:, :2]
        bb = [np.asarray(centri[1], float)]
    out, lontano = [], np.ones(n, dtype=bool)
    for b in bb:
        r = np.hypot(*(dxy - b).T)
        dentro = r < R_LOC
        lontano &= r > R_LONTANO
        comp = int(np.argmax([np.sum(np.abs(pn[dentro, j]) ** 2) for j in (0, 1)]))
        out.append((b, float(np.angle(np.sum(rho[dentro] * pn[dentro, comp]))), float(np.angle(np.sum(rho[dentro] * zn[dentro])))))
    return out, float(np.angle(np.sum(zn[lontano]))) if lontano.any() else float("nan"), int(lontano.sum())


def main():
    import _presidio
    import mattone as MT
    from solitone import convergenza as CV
    for m in ("pound_rebka_GU.py", "orologio_mattone.py", "girandola_chi_v3.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    w0, _rms, _sd = PR.omega_ref()
    print("=" * 130)
    print("[M1417-R] L'OROLOGIO RELATIVO AL VUOTO (la carta sez. 7; POST-HOC, dichiarato da Luca): omega_ref (N1) %.10f" % w0)
    print("=" * 130)
    # ### K1: N1
    with TC.scena() as Z:
        t0 = TC.moduli()[0].G2.T0
        L = Z["L"]
        nodo = GC.toro_nodo(L)
        F = np.load(os.path.join(OM.BASE, "N1", "fase.npy"))
        Phi = np.unwrap(np.angle(F))
        ac = arg_c(Z, t0, t0 + OM.K_FINO)
        ks, Psi = [], []
        for k in (250, 500, 750, 1000):
            X, meta = PR_leggi(os.path.join(OM.BASE, "N1", "stato_%06d.npz" % k))
            o, _tl, _nl = fasi(Z, X["psi_h"], X["phi_h"], t0 + k, nodo, L, centri=(meta["centro"], meta["bari_k0"]))
            ks.append(k)
            Psi.append(o[0][2])
        tv = np.unwrap(np.array(Psi))
        rel = np.array([ac[k] + tv[i] - Phi[k] for i, k in enumerate(ks)])
        A = np.stack([np.ones(len(ks)), np.array(ks, float)], axis=1)
        b, *_ = np.linalg.lstsq(A, rel, rcond=None)
        res = rel - A @ b
        wF3 = -float(ac[-1] - ac[0]) / OM.K_FINO
        print("### K1, N1 da solo: omega_F3 %.10f; theta_v locale %s; omega_rel (la pendenza) %+.8f; il residuo del fit %.3e rad" % (wF3, ", ".join("%+.5f" % x for x in tv), -float(b[1]), float(np.sqrt(res @ res / max(len(ks) - 2, 1)))))
        esito("K1: l'orologio N1 da solo, omega_rel costante (il residuo del fit della fase relativa sotto 1 rad)", float(np.sqrt(res @ res / max(len(ks) - 2, 1))) < 1.0)
        Z["metti"]()
    # ### le coppie
    RIS = {}
    for mondo, nome, ks in PR.COPPIE:
        cm = CV.scena_L(243, 100.5) if mondo == "GUd65" else MT.scena("C35-pi", 60000)
        with cm as Z:
            print("-" * 130)
            righe = []
            for k in ks:
                f = os.path.join(PR.DIR, "coppia%s_L162_%05d.npz" % (mondo, k))
                with np.load(f) as z:
                    psi_h, phi_h = z["psi_h"], z["phi_h"]
                    t = int(json.loads(str(z["meta"]))["t"])
                L = int(round(math.sqrt(psi_h.shape[0] // 6)))
                assert L == Z["L"], "il toro dello stato %d non e' quello della scena %d" % (L, Z["L"])
                o, tl, nl = fasi(Z, psi_h, phi_h, t, GC.toro_nodo(L), L)
                righe.append((k, t, o, tl))
                print("  %-26s k %4d (t %d, sha1 %s): psi %+.5f %+.5f; theta_v locale %+.5f %+.5f; lontano %+.5f (%d nodi)" % (nome, k, t, PR.sha1(f)[:8], o[0][1], o[1][1], o[0][2], o[1][2], tl, nl))
            om = []
            for (ka, ta, oa, tla), (kb, tb, ob, tlb) in zip(righe, righe[1:]):
                dk = kb - ka
                ac = arg_c(Z, ta, tb)
                wF3 = -float(ac[-1] - ac[0]) / dk
                wpsi = [w0 + PR.wrap(-(ob[j][1] - oa[j][1]) - w0 * dk) / dk for j in (0, 1)]
                dv = [PR.wrap(ob[j][2] - oa[j][2]) for j in (0, 1)]
                dvl = PR.wrap(tlb - tla)
                wphi = [wF3 - x / dk for x in dv]
                wfar = wF3 - dvl / dk
                rel = [wphi[j] - wpsi[j] for j in (0, 1)]
                om.append(dict(ka=ka, kb=kb, wF3=wF3, wpsi=wpsi, wphi=wphi, wfar=wfar, rel=rel, dv=dv + [dvl]))
                print("    k %4d -> %4d: omega_F3 %.10f; omega_psi %.8f %.8f; omega_phi locale %.8f %.8f (theta_v si sposta di %+.4f %+.4f rad); lontano %.8f (%+.4f rad); omega_rel %+.8f %+.8f" % (
                    ka, kb, wF3, wpsi[0], wpsi[1], wphi[0], wphi[1], dv[0], dv[1], wfar, dvl, rel[0], rel[1]))
            Z["metti"]()
        RIS[mondo] = (nome, om)
    print("=" * 130)
    amb = max(abs(x) for _n, om in RIS.values() for o in om for x in o["dv"])
    esito("il controllo: ogni spostamento di theta_v fra due stati sotto pi/2 (omega_v senza ambiguita')", amb < math.pi / 2, "(il massimo %.4f rad)" % amb)
    far = {m: float(np.mean([o["wfar"] for o in om])) for m, (_n, om) in RIS.items()}
    sp = max(far.values()) - min(far.values())
    print("  il vuoto lontano, omega_phi per coppia: %s; lo scarto massimo %.3e" % (", ".join("%s %.10f" % (m, v) for m, v in far.items()), sp))
    esito("K2: omega_phi nel vuoto lontano uguale fra le coppie entro 1e-5", sp <= TOLL_K2, "(%.3e)" % sp)
    med = {m: (float(np.mean([np.mean(o["rel"]) for o in om])), float(np.mean([np.mean(o["wphi"]) for o in om])), float(np.mean([np.mean(o["wpsi"]) for o in om]))) for m, (_n, om) in RIS.items()}
    base = [0.5 * (med["GUd50"][i] + med["GUd65"][i]) for i in range(3)]
    print("  LA BASE (d 50 e d 66): omega_rel %+.8f; omega_phi locale %.8f; omega_psi %.8f; IL SEGNO DI omega_phi - omega_psi DI BASE: %s" % (base[0], base[1], base[2], "+" if base[0] > 0 else "-"))
    for m, (nome, _om) in RIS.items():
        print("  %-26s omega_rel %+.8f, Delta omega_rel %+.4e; Delta omega_phi locale %+.4e; Delta omega_psi %+.4e" % (nome, med[m][0], med[m][0] - base[0], med[m][1] - base[1], med[m][2] - base[2]))
    d = med["GU"][0] - base[0]
    print("  K3 (la coppia che si attrae, B2 a d 34): Delta omega_rel %+.4e: %s; P3: |Delta omega_phi locale| %.3e contro |Delta omega_psi| %.3e" % (
        d, "NEGATIVO: come la natura (l'orologio relativo rallenta legandosi)" if d < 0 else "POSITIVO: come prima", abs(med["GU"][1] - base[1]), abs(med["GU"][2] - base[2])))
    print("-" * 130)
    for c_, ok in ESITI:
        print("  DEVE: %-110s %s" % (c_, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def PR_leggi(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == PR.sha1(f), "lo sha1 di %s NON coincide" % f
    z = np.load(f)
    X = {x: z[x] for x in z.files}
    return X, json.loads(str(X.pop("meta")))


if __name__ == "__main__":
    sys.exit(main())
