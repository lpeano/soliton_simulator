# -*- coding: utf-8 -*-
r"""**[M1427-R] IL VERSO DELL'OROLOGIO: QUALE ZERO** *(la decisione di Luca [M1427]; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `8`; SOLA LETTURA; POST-HOC, dichiarato da Luca)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/orologio_zero.py > doc/referti_l2/orologio_zero.txt

**Gli zeri** `omega0 = omega(1) - d omega/dN` per V1, V2, V3 *(misurati: le fasi dell'orologio, `fase.npy` con lo sha1)* e V4 *(RICAVATO: `d omega/dN(V2) - d omega/dN(V3)`)*. **K1:** `|a(V2)/a(V3)|` della caduta *(letto da `caduta_libera.txt`)* contro il rapporto delle distanze dallo zero. **T1:** `Delta|omega_psi - omega0|` per coppia *(`omega_psi` letto da `pound_rebka_GU.txt`)* e `Delta|omega_psi - omega_phi|` *(letto da `orologio_relativo.txt`)*. **K2** letto da `orologio_relativo.txt`.
"""
import hashlib
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402,F401  (i percorsi)
import orologio_mattone_v2 as OM  # noqa: E402

ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def testo(nome):
    f = os.path.join(_QUI, nome)
    print("### il referto %s (sha1 %s)" % (nome, sha1(f)[:8]))
    return open(f, encoding="utf-8", errors="replace").read()


def omega(var):
    f = os.path.join(OM.BASE, var, "fase.npy")
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f
    ph = np.unwrap(np.angle(np.load(f)))
    k = np.arange(len(ph), dtype=float)
    m = k >= OM.K_DA_FIT
    A = np.stack([np.ones(m.sum()), k[m]], axis=1)
    b, *_ = np.linalg.lstsq(A, ph[m], rcond=None)
    return -float(b[1])


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "orologio_mattone_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1427-R] IL VERSO DELL'OROLOGIO: QUALE ZERO (la carta sez. 8; POST-HOC, dichiarato da Luca)")
    print("=" * 130)
    w = {v: omega(v) for v in ("N1", "Nm", "Np", "NmV2", "NmV3", "NpV3")}
    Nm, Np = OM.VAR["Nm"][0], OM.VAR["Np"][0]
    d = {"V1": (w["Np"] - w["Nm"]) / (Np - Nm), "V2": (w["NmV2"] - w["N1"]) / (Nm - 1.0), "V3": (w["NpV3"] - w["NmV3"]) / (Np - Nm)}
    d["V4"] = d["V2"] - d["V3"]
    z = {f: w["N1"] - x for f, x in d.items()}
    print("### l'orologio: omega(N1) %.10f; %s" % (w["N1"], "; ".join("%s %.10f" % (v, x) for v, x in w.items() if v != "N1")))
    for f in ("V1", "V2", "V3", "V4"):
        print("    %s: d omega/dN %+.8f%s; LO ZERO omega0 = omega(1) - d omega/dN = %+.8f; omega(1) - omega0 = %+.8f (%s psi)" % (
            f, d[f], " (RICAVATO: V2 - V3)" if f == "V4" else "", z[f], w["N1"] - z[f], "lo zero SOTTO" if z[f] < w["N1"] else "lo zero SOPRA"))
    # ### K1
    cad = testo("caduta_libera.txt")
    a = {}
    for f in ("V2", "V3"):
        m = re.search(r"^\s+%s\s+il baricentro\s+a [-+0-9.e]+ \+- [0-9.e+-]+; a - a\(V0\) ([-+0-9.e]+) \+- ([0-9.e+-]+)" % f, cad, re.M)
        a[f] = (float(m.group(1)), float(m.group(2)))
    ra = abs(a["V2"][0] / a["V3"][0])
    sra = ra * math.hypot(a["V2"][1] / a["V2"][0], a["V3"][1] / a["V3"][0])
    rd = abs(w["N1"] - z["V2"]) / abs(w["N1"] - z["V3"])
    print("### K1: la caduta |a(V2)/a(V3)| = %.5f +- %.5f (a - a(V0): %+.4e, %+.4e); le distanze dallo zero |omega(1) - omega0(V2)| / |omega(1) - omega0(V3)| = %.5f; lo scarto %+.3e" % (
        ra, sra, a["V2"][0], a["V3"][0], rd, rd / ra - 1.0))
    esito("K1: V2/V3 della caduta = il rapporto delle distanze dallo zero entro l'1%", abs(rd / ra - 1.0) <= 0.01, "(%+.3e)" % (rd / ra - 1.0))
    # ### T1
    pr = testo("pound_rebka_GU.txt")
    wref = float(re.search(r"omega_ref \(l'orologio N1, il mattone da solo\) ([0-9.]+) per tick", pr).group(1))
    cop = {}
    for m in re.finditer(r"^\s{4}(.+?)\s+d medio ([0-9.]+): omega - omega_ref ([-+0-9.e]+)", pr, re.M):
        cop[m.group(1).strip()] = (float(m.group(2)), wref + float(m.group(3)))
    rel = testo("orologio_relativo.txt")
    mb = re.search(r"LA BASE \(d 50 e d 66\): omega_rel ([-+0-9.e]+); omega_phi locale ([-+0-9.e]+); omega_psi ([-+0-9.e]+)", rel)
    phi_b, psi_b = float(mb.group(2)), float(mb.group(3))
    dphi = {}
    for m in re.finditer(r"^\s{2}(.+?)\s+omega_rel [-+0-9.e]+, Delta omega_rel ([-+0-9.e]+); Delta omega_phi locale ([-+0-9.e]+); Delta omega_psi ([-+0-9.e]+)", rel, re.M):
        dphi[m.group(1).strip()] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
    k2 = float(re.search(r"il vuoto lontano, omega_phi per coppia: .*; lo scarto massimo ([0-9.e+-]+)", rel).group(1))
    esito("K2: omega_phi nel vuoto lontano uguale fra le coppie entro 1e-5 (da orologio_relativo.txt)", k2 <= 1e-5, "(%.3e)" % k2)
    base_nomi = [n for n in cop if "d 50" in n or "d 65" in n]
    base = float(np.mean([cop[n][1] for n in base_nomi]))
    print("### la base (%s): omega_psi %.8f; omega_phi locale (orologio_relativo) %.8f" % (", ".join(base_nomi), base, phi_b))
    print("-" * 130)
    print("  T1: Delta|omega_psi - omega0| = |omega_psi(coppia) - omega0| - |omega_psi(base) - omega0|; NEGATIVO = come la natura, POSITIVO = al contrario")
    verd = {}
    for n, (dm, wp) in cop.items():
        righe = []
        for f in ("V1", "V2", "V3", "V4"):
            x = abs(wp - z[f]) - abs(base - z[f])
            righe.append("%s %+.4e" % (f, x))
            if "B2 in fase" in n:
                verd[f] = x
        dv = dphi.get(n)
        vac = (abs((psi_b + dv[2]) - (phi_b + dv[1])) - abs(psi_b - phi_b)) if dv else float("nan")
        if "B2 in fase" in n:
            verd["vuoto"] = vac
        print("    %-26s d %.3f, omega_psi %.8f (Delta %+.4e): %s; il vuoto locale %+.4e" % (n, dm, wp, wp - base, "; ".join(righe), vac))
    print("-" * 130)
    print("  K3, LA COPPIA CHE SI ATTRAE (B2 in fase): " + "; ".join("%s %s" % (f, ("NEGATIVO: come la natura" if x < 0 else "POSITIVO: al contrario")) for f, x in verd.items()))
    print("  il verdetto %s da una forma all'altra" % ("CAMBIA" if len(set(x < 0 for x in verd.values())) > 1 else "NON cambia"))
    print("-" * 130)
    for c_, ok in ESITI:
        print("  DEVE: %-110s %s" % (c_, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


if __name__ == "__main__":
    sys.exit(main())
