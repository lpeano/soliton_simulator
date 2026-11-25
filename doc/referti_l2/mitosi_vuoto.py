# -*- coding: utf-8 -*-
r"""**[M0237-4] NASCE QUALCOSA NEL VUOTO PURO?** *(DECISIONE DI LUCA, 2026-11-25 02:37, dalla posta; la carta `doc/CARTA_mitosi.md`, «Le tre prove»)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto.py prepara > doc/referti_l2/mitosi_vuoto_prepara.txt
    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto.py noto      (K4: nascite spente, da 35976 a 36250; dalla coda)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto.py corsa     (nascite accese, 6000 tick; dalla coda, dopo K4)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto.py lettura > doc/referti_l2/mitosi_vuoto.txt

**Lo stato del vuoto** *(`prepara`: `E:/soliton_simulator/controllo/M0237/vuoto/vuoto_35976.npz`, con lo sha1)*: la `prima_nascita_35976.npz` del TRONCO con **`psi_h`, `psi`, `rho` a zero**; **`phi_h = a phi_v`**, con `a` il fit complesso di `phi_h` del tronco su `phi_v` sui nodi a distanza `> 45` dal centro dell'oggetto *(«le stesse fasi del tronco»; il residuo stampato)*; **`campo_A`, `campo_E` a zero** *(senza materia, Gauss da' zero)*; **`theta_a` a zero** *(il contatore del tronco e' accumulato con la materia: tenerlo farebbe scattare gli archi subito, e la domanda non avrebbe senso)*. **Le altre chiavi** *(`Lambda`, `h_int`, `cs_prec`, `gauss_acc`)* e il meta: quelle del tronco, dichiarato. **La corsa:** `mitosi_lunga.corsa` cosi' com'e', da quello stato. **(K4):** con le nascite spente, `250` tick *(da `36000` a `36250`)*: `somma |phi_h|^2` e `H` *(la serie `E`)* fermi entro `1e-9` relativo.
"""
import argparse
import glob
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "..", "..", "csv")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))
import mitosi_dati as MD  # noqa: E402

SORGENTE = os.path.join(MD.R, "TRONCO", "prima_nascita_35976.npz")
BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0237")
F_VUOTO = os.path.join(BASE, "vuoto", "vuoto_35976.npz")
K0 = 35976
R_FONDO = 45.0


def sha1(f):
    import hashlib
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def prepara():
    import mitosi_lunga as ML
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "mitosi_lunga.py"))
    _presidio.avvia(__file__)
    assert not os.path.exists(F_VUOTO), "%s c'e' gia': non si riscrive" % F_VUOTO
    assert open(SORGENTE + ".sha1", encoding="utf-8").read().split()[0] == sha1(SORGENTE)
    with np.load(SORGENTE) as d:
        X = {x: d[x].copy() for x in d.files}
    meta = json.loads(str(X["meta"]))
    PS = ML.PS
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        pv = np.asarray(Z["phi_v"]).copy()
        nodo = np.asarray(Z["mot"].inc.nodo)
        L = Z["L"]
        v = np.arange(L * L)
        c = meta["centro"]
        d = np.hypot(*np.asarray(TO.scarti((v // L).astype(float), (v % L).astype(float), c[0], c[1], L))[:, :2].T)
        Z["metti"]()
    assert pv.shape == X["phi_h"].shape and len(d) == int(nodo.max()) + 1
    lon = (d > R_FONDO)[nodo]
    a = complex(np.sum(np.conj(pv[lon]) * X["phi_h"][lon]) / np.sum(np.abs(pv[lon]) ** 2))
    res = np.abs(X["phi_h"][lon] - a * pv[lon]) / np.abs(a * pv[lon])
    print("=" * 130)
    print("[M0237-4] LO STATO DEL VUOTO PURO da %s (k %s, t %s)" % (SORGENTE, meta.get("k"), meta.get("t")))
    print("=" * 130)
    print("  a del fondo %+.9f%+.9fi (|a| %.9f); il residuo del fit a d > %.0f: medio %.3e, massimo %.3e" % (a.real, a.imag, abs(a), R_FONDO, float(res.mean()), float(res.max())))
    print("  la materia del tronco: somma |psi_h|^2 %.9e (si azzera); la norma del vuoto: somma |phi_h|^2 %.9e -> %.9e" % (float(np.sum(np.abs(X["psi_h"]) ** 2)), float(np.sum(np.abs(X["phi_h"]) ** 2)), float(np.sum(np.abs(a * pv) ** 2))))
    Y = dict(X)
    for x in ("psi_h", "psi", "rho"):
        Y[x] = np.zeros_like(X[x])
    Y["phi_h"] = a * pv
    Y["campo_A"] = np.zeros_like(X["campo_A"])
    Y["campo_E"] = np.zeros_like(X["campo_E"])
    Y["theta_a"] = np.zeros_like(X["theta_a"])
    Y["meta"] = np.array(json.dumps(dict(meta, vuoto_da=SORGENTE, a_fondo=[a.real, a.imag])))
    os.makedirs(os.path.dirname(F_VUOTO), exist_ok=True)
    np.savez(F_VUOTO, **Y)
    open(F_VUOTO + ".sha1", "w", encoding="utf-8").write(sha1(F_VUOTO) + "\n")
    print("### scritto %s (sha1 %s); le chiavi %s" % (F_VUOTO, sha1(F_VUOTO)[:8], sorted(Y)))
    print("=" * 130)
    return 0


def corsa(nascite, fino, nome):
    import mitosi_lunga as ML
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_lunga.py"))
    _presidio.avvia(__file__)
    d = os.path.join(ML.DIR, nome)
    assert not glob.glob(os.path.join(d, "stato_*.npz")), "%s ha gia' degli stati: non si riscrive" % d
    os.makedirs(d, exist_ok=True)
    print("### [M0237-4] il vuoto puro, le nascite %s, da %d a %d; la sorgente %s; le uscite in %s" % ("ACCESE" if nascite else "SPENTE", K0, fino, F_VUOTO, d))
    sys.stdout.flush()
    return ML.corsa(nome, K0, fino, nascite, None, F_VUOTO)


def noto():
    r = corsa(False, 36250, "M0237" + os.sep + "vuoto_noto")
    a = np.load(os.path.join(BASE, "vuoto_noto", "stato_36000.npz"))
    b = np.load(os.path.join(BASE, "vuoto_noto", "stato_36250.npz"))
    na, nb = float(np.sum(np.abs(a["phi_h"]) ** 2)), float(np.sum(np.abs(b["phi_h"]) ** 2))
    with np.load(os.path.join(BASE, "vuoto_noto", "serie_36250.npz")) as z:
        k, E = z["k"], z["E"]
    ea, eb = float(E[k == 36000][0]), float(E[k == 36250][0])
    rn, re = abs(nb / na - 1.0), abs(eb / ea - 1.0)
    ok = r == 0 and rn < 1e-9 and re < 1e-9
    print("  DEVE: (K4) il vuoto senza nascite, 250 tick (36000 -> 36250): la norma %.12e -> %.12e (%.2e), H %+.12e -> %+.12e (%.2e), entro 1e-9   %s" % (na, nb, rn, ea, eb, re, "PASSA" if ok else "### FALLISCE"))
    return 0 if ok else 1


def lettura():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0237-4] IL VUOTO PURO CON LE NASCITE ACCESE, 6000 TICK (la carta doc/CARTA_mitosi.md)")
    print("=" * 130)
    d = os.path.join(BASE, "vuoto")
    ff = sorted(glob.glob(os.path.join(d, "nascite_*.json")))
    b = json.load(open(ff[-1], encoding="utf-8")) if ff else []
    st = sorted(glob.glob(os.path.join(d, "stato_*.npz")))
    print("  gli stati: %d (%s .. %s); le nascite: %d" % (len(st), os.path.basename(st[0]) if st else "-", os.path.basename(st[-1]) if st else "-", len(b)))
    for x in b[:20]:
        print("    k %d: l'arco %s, r %.2f, DH %+.4e" % (int(x["k"]), x["a"], float(x.get("r", float("nan"))), float(x["DH"])))
    pn = sorted(glob.glob(os.path.join(d, "prima_nascita_*.npz")))
    if pn:
        with np.load(pn[0]) as z:
            rho = np.abs(z["psi_h"]) ** 2
            print("  alla prima nascita (%s): somma |psi_h|^2 %.6e, max %.6e" % (os.path.basename(pn[0]), float(rho.sum()), float(rho.max())))
    print("### NASCITE NEL VUOTO PURO: %s" % ("SI', %d, la prima a k %d" % (len(b), int(b[0]["k"])) if b else "NESSUNA"))
    print("=" * 130)
    return 0


def main(argv):
    os.chdir(os.path.abspath(os.path.join(_QUI, "..", "..")))     # ### dal lanciatore di lapse-u: la radice di QUESTO worktree (mitosi)
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("prepara", "noto", "corsa", "lettura"))
    a = ap.parse_args(argv)
    if a.cosa == "corsa":
        return corsa(True, K0 + 6000, "M0237" + os.sep + "vuoto")
    return {"prepara": prepara, "noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
