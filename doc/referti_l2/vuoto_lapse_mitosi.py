# -*- coding: utf-8 -*-
r"""**[M0026] F: LA NASCITA NEL VUOTO CON IL LAPSE DIPINTO** *(DECISIONE DI LUCA, 2026-11-28 00:26, la via (a); il task history
`doc/TASK_HISTORY/2026-11-28_m0026_corpo_fuso_nascite.md`; la carta `doc/CARTA_mitosi.md`, «F, LA VIA (a)»)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/vuoto_lapse_mitosi.py noto > doc/referti_l2/vuoto_lapse_mitosi_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/vuoto_lapse_mitosi.py corsa           (dalla coda: 6000 tick)

**La corsa del vuoto di [M0106]** *(`mitosi_rami_v2.ciclo("...", "mitosi", M0237/vuoto/vuoto_35976.npz, ..., nascita_iniziale=False)`, `L 186`,
le nascite ACCESE, nessuna materia)* **con il lapse dipinto DENTRO il tick della mitosi:** durante la corsa `tick_lapse.N_di(rho, legge)` ->
`N_di(rho, legge) * N_dip(x)` e `Np_di` -> `Np_di * N_dip(x)`, con `N_dip = exp(-kappa chi_dip)`, `chi_dip = A sin(2 pi (y - y_c) / L_y)`
*(la forma di `caduta_libera.campo_N`)*, `y = m2 sqrt(3)/2` dei nodi della scena *(catturata avvolgendo `convergenza.scena_L`)*.
**Nel vuoto la materia e' zero e `N_di = 1`: il lapse E' quello dipinto.** **Il nodo nato** *(la chiamata di `applica` su un solo nodo)*: `N_dip`
nella posizione di `posizioni.nuova(m1, m2, i, j, L)` *(F-3: derivato)*. **L'ampiezza (F-2):** lo stesso GRADIENTE `G20` di [M2210],
`A = G20 L_y / (2 pi kappa)` con `L_y` di `L 186`; `y_c = 0` *(una fase: dichiarata)*.
**`noto`:** (K-F0) con `A = 0` il fattore e' `1.0` esatto e i primi `250` tick *(fino a `k 36250`)* = la corsa di [M0106]
*(`M0237/vuoto_v2/stato_36250.npz`)* AL BIT; (K-F1) DEVE FALLIRE: con `A` vero lo stato a `36250` e' diverso; (K-F2) `N_dip` sui nodi =
`caduta_libera.campo_N` sulla stessa scena AL BIT. **`corsa`:** `6000` tick da `k 35976`, gli stati ogni `250`, in `controllo/M0026/F`.
"""
import argparse
import contextlib
import glob
import math
import os
import shutil
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_rami_v2 as RV  # noqa: E402
import mitosi_vuoto_v2 as MV2  # noqa: E402

PS, MR = RV.PS, RV.MR
CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
D_OUT = os.path.join(CTRL, "M0026", "F")
D_NOTO = os.path.join(CTRL, "M0026", "F_noto")
D_M0106 = os.path.join(CTRL, "M0237", "vuoto_v2")
K0, K_CTRL, K_FINE = 35976, 36250, 35976 + 6000
Y_C = 0.0
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def ampiezza(L):
    """### lo stesso GRADIENTE `G20` di [M2210] (`caduta_libera`): `A = G20 L_y / (2 pi kappa)`."""
    import caduta_libera as CLb
    G20, _ia = CLb.ampiezza()
    Ly = L * math.sqrt(3.0) / 2.0
    return G20 * Ly / (2.0 * math.pi * CLb.CP2.KAPPA), G20, Ly, CLb.CP2.KAPPA


@contextlib.contextmanager
def dipinto(A):
    """### `N_di`, `Np_di` per il seno dipinto; la scena catturata da `convergenza.scena_L`; il nodo nato dalla sua posizione."""
    from solitone import tick_lapse as TL
    from solitone import posizioni as PZ
    import caduta_libera as CLb
    CV = PS.CV
    box = {"Z": None, "nato": None, "cache": {}}
    scena0, N0, Np0, applica0 = CV.scena_L, TL.N_di, TL.Np_di, MR.applica

    @contextlib.contextmanager
    def scena(*a, **kw):
        with scena0(*a, **kw) as Z:
            box["Z"] = Z
            yield Z

    def f_dip(m2, L):
        y = np.asarray(m2, dtype=float) * math.sqrt(3.0) / 2.0
        Ly = L * math.sqrt(3.0) / 2.0
        return np.exp(-CLb.CP2.KAPPA * (float(A) * np.sin(2.0 * math.pi * (y - Y_C) / Ly)))

    def fattore(size):
        Z = box["Z"]
        if size == 1 and box["nato"] is not None:
            i, j = box["nato"]
            _p1, p2 = PZ.nuova(Z["m1"], Z["m2"], i, j, Z["L"])
            return f_dip(np.array([p2]), Z["L"])
        m2 = np.asarray(Z["m2"], dtype=float)
        assert m2.size == size, "N_di su %d valori, la scena ha %d nodi: il lapse dipinto non sa dove sono" % (size, m2.size)
        k = (size, float(m2[-1]))
        if k not in box["cache"]:
            box["cache"] = {k: f_dip(m2, Z["L"])}
        return box["cache"][k]

    def applica(Z, C, cont, S):
        box["nato"] = (int(S["nodi"]["i"]), int(S["nodi"]["j"]))
        try:
            return applica0(Z, C, cont, S)
        finally:
            box["nato"] = None

    CV.scena_L = scena
    TL.N_di = lambda rho, legge: N0(rho, legge) * fattore(np.asarray(rho).size)
    TL.Np_di = lambda rho, legge: Np0(rho, legge) * fattore(np.asarray(rho).size)
    MR.applica = applica
    try:
        yield box, f_dip
    finally:
        CV.scena_L, TL.N_di, TL.Np_di, MR.applica = scena0, N0, Np0, applica0


def avvia():
    import _presidio
    for m in ("mitosi_rami_v2.py", "mitosi_vuoto_v2.py", "caduta_libera.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def confronta(fa, fb):
    out = []
    with np.load(fa) as a, np.load(fb) as b:
        for x in a.files:
            if x == "meta":
                continue
            if x not in b.files or not np.array_equal(a[x], b[x]):
                out.append(x)
    return out


def corri(A, d, fino):
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d, exist_ok=True)
    with dipinto(A) as (box, f_dip):
        cod, k, _f = RV.ciclo("vuoto_lapse_" + os.path.basename(d), "mitosi", MV2.F_VUOTO, fino, None, nascita_iniziale=False, d_out=d)
    return cod, k


def noto():
    avvia()
    print("=" * 134)
    print("[M0026] F, I CASI NOTI: K-F0 (A = 0 = [M0106] al bit), K-F1 (A vero: diverso), K-F2 (N_dip = campo_N)")
    print("=" * 134)
    A, G20, Ly, kappa = ampiezza(186)
    print("  L 186: L_y %.6f; G20 %.6e; kappa %r; A = G20 L_y / (2 pi kappa) = %.6e; y_c %.1f" % (Ly, G20, kappa, A, Y_C))
    f0 = os.path.join(D_M0106, "stato_%05d.npz" % K_CTRL)
    cod, k = corri(0.0, os.path.join(D_NOTO, "A0"), K_CTRL)
    fa = os.path.join(D_NOTO, "A0", "stato_%05d.npz" % K_CTRL)
    d = confronta(fa, f0)
    esito("(K-F0) A = 0: lo stato a k %d = [M0106] (%s) AL BIT" % (K_CTRL, f0), cod == 0 and not d, "il codice %d; diverse %s" % (cod, d))
    cod, k = corri(A, os.path.join(D_NOTO, "A"), K_CTRL)
    fb = os.path.join(D_NOTO, "A", "stato_%05d.npz" % K_CTRL)
    d = confronta(fb, f0)
    esito("(K-F1) DEVE FALLIRE: con A vero lo stato a k %d e' DIVERSO da [M0106]" % K_CTRL, bool(d), "diverse %s" % d)
    import caduta_libera as CLb
    with dipinto(A) as (box, f_dip):
        with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
            nd = f_dip(Z["m2"], Z["L"])
            _chi, Nc = CLb.campo_N(Z, {"y_c": Y_C}, A, 1.0)
            Z["metti"]()
    esito("(K-F2) N_dip sui nodi = caduta_libera.campo_N sulla stessa scena AL BIT", np.array_equal(nd, Nc), "N da %.10f a %.10f" % (float(nd.min()), float(nd.max())))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


def corsa():
    avvia()
    assert not glob.glob(os.path.join(D_OUT, "stato_*.npz")), "%s ha gia' degli stati: non si riscrive" % D_OUT
    A, G20, Ly, kappa = ampiezza(186)
    print("### [M0026] F: il vuoto di [M0106] con il lapse dipinto (A %.6e, G20 %.6e, L_y %.6f, kappa %r, y_c %.1f), le nascite accese, da k %d a %d, in %s" % (
        A, G20, Ly, kappa, Y_C, K0, K_FINE, D_OUT))
    sys.stdout.flush()
    os.makedirs(D_OUT, exist_ok=True)
    with dipinto(A) as (box, f_dip):
        cod, k, _f = RV.ciclo("vuoto_lapse_F", "mitosi", MV2.F_VUOTO, K_FINE, None, nascita_iniziale=False, d_out=D_OUT)
    print("### il codice %d, k %d" % (cod, k))
    return cod


def main(argv):
    a = argparse.ArgumentParser()
    a.add_argument("modo", choices=("noto", "corsa"))
    x = a.parse_args(argv)
    return noto() if x.modo == "noto" else corsa()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
