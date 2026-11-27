# -*- coding: utf-8 -*-
r"""**[M2245-B] IL VUOTO SI AMMASSA?** *(DECISIONE DI LUCA, 2026-11-24 22:49; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-duodecies`; A dice che il vuoto scorre: B si fa; solo letture)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/vuoto_ammassato.py > doc/referti_l2/vuoto_ammassato.txt

**Le corse** *(dichiarate nella carta)*: **chi VERO** = gli stati con le chiavi `chi` e `pi` *(il campo con la sua equazione del moto)*: **`CHI/due_corpi/F-on` contro `F-off`** *([M0417]: due mattoni a `39` nodi, `chi` acceso contro `kappa = 0`; `13` stati, `k 0..3000`)*. **Accanto, chi IMPOSTO:** `CHI/caduta/V2` e `V0` *(`caduta_libera`, nominata da Luca; `9` stati, `k 0..2000`)*. **Per stato:** `rho_phi = somma |phi_h|^2` per nodo, **la media sugli anelli `[0, 8)`, `[8, 16)`, `[16, 32)`** attorno al baricentro di `rho_psi` *(`toro.centro`, `toro.scarti`)*. **Con due corpi:** il centro della coppia, poi ogni corpo nella sua meta' *(il segno di `dx` dal centro)*, il suo baricentro, e gli anelli dentro la sua meta'.
"""
import glob
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
CORSE = (("CHI/due_corpi/F-on", 2), ("CHI/due_corpi/F-off", 2), ("CHI/caduta/V2", 1), ("CHI/caduta/V0", 1))
ANELLI = ((0.0, 8.0), (8.0, 16.0), (16.0, 32.0))


def sha1(f):
    import hashlib
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def anelli(rho_phi, d, dentro):
    return [float(rho_phi[dentro & (d >= a) & (d < b)].mean()) for a, b in ANELLI]


def corpi(rpsi, m1, m2, L, quanti):
    """### `[(d, dentro)]` per corpo: la distanza dal baricentro del corpo e la maschera dei nodi che gli spettano."""
    from solitone import toro as TO
    b = TO.centro(rpsi, m1, m2, L)[:2]
    dxy = TO.scarti(m1, m2, b[0], b[1], L)[:, :2]
    if quanti == 1:
        return [(np.hypot(dxy[:, 0], dxy[:, 1]), np.ones(len(rpsi), bool))]
    out = []
    for lato in (dxy[:, 0] < 0.0, dxy[:, 0] >= 0.0):
        w = rpsi * lato
        c = (dxy * w[:, None]).sum(axis=0) / w.sum()
        out.append((np.hypot(dxy[:, 0] - c[0], dxy[:, 1] - c[1]), lato))
    return out


def main():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2245-B] IL VUOTO SI AMMASSA? (la carta sez. 3-duodecies): rho_phi sugli anelli [0,8), [8,16), [16,32) attorno a ogni corpo, per stato")
    print("=" * 130)
    with TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"]), np.asarray(Z["m2"])
        Z["metti"]()
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    dd = np.arange(n, dtype=float) % 40.0
    tutto = np.ones(n, bool)
    esito("(a) rho_phi costante = 2.5: le tre medie = 2.5 AL BIT", anelli(np.full(n, 2.5), dd, tutto) == [2.5, 2.5, 2.5])
    a = anelli(dd.copy(), dd, tutto)
    esito("(b) DEVE FALLIRE la costanza: rho_phi = d da' tre medie diverse e crescenti", a[0] < a[1] < a[2], "%s" % a)
    for cartella, quanti in CORSE:
        d_ = os.path.join(CTRL, *cartella.split("/"))
        ff = sorted(glob.glob(os.path.join(d_, "stato_*.npz")))
        print("-" * 130)
        print("  %s (%d corp%s): %d stati, da %s a %s" % (cartella, quanti, "o" if quanti == 1 else "i", len(ff), os.path.basename(ff[0]), os.path.basename(ff[-1])))
        print("-" * 130)
        R0 = None
        for f in ff:
            if os.path.exists(f + ".sha1"):
                assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
            k = int(os.path.basename(f)[6:12])
            with np.load(f) as z:
                psi_h, phi_h = z["psi_h"], z["phi_h"]
                assert "chi" in z.files
                vero = "pi" in z.files
            rpsi = np.bincount(nodo, weights=np.sum(np.abs(psi_h) ** 2, axis=1), minlength=n)
            rphi = np.bincount(nodo, weights=np.abs(phi_h) ** 2, minlength=n)
            C = corpi(rpsi, m1, m2, L, quanti)
            v = [anelli(rphi, d, m) for d, m in C]
            if R0 is None:
                R0 = v
            print("  k %5d (%s): %s; la somma di rho_phi %.6f" % (k, "chi vero" if vero else "chi imposto", "  |  ".join(
                "corpo %d: %s" % (j + 1, " ".join("%.6f (%+.3f%%)" % (x, 100.0 * (x / x0 - 1.0)) for x, x0 in zip(v[j], R0[j]))) for j in range(quanti)), float(rphi.sum())))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
