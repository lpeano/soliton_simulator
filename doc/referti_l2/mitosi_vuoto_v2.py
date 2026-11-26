# -*- coding: utf-8 -*-
r"""**[M0237-4] IL VUOTO PURO, LA V2: SULLA VIA VERA, COL RESIDUO DI GAUSS ASSOLUTO** *([M2034], DECISIONE DI LUCA 2026-11-26 20:34, D2; la carta `doc/CARTA_mitosi.md`, «D1 e D2»; `mitosi_vuoto.py` e' usato e non si riscrive)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto_v2.py noto > doc/referti_l2/mitosi_vuoto_v2_noto.txt       (K4)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto_v2.py corsa       (le nascite accese, 6000 tick; dalla coda, dopo d1', d2', d3')
    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto_v2.py lettura > doc/referti_l2/mitosi_vuoto_v2.txt

**Lo stato:** `M0237/vuoto/vuoto_35976.npz` *(gia' preparato da `mitosi_vuoto.py prepara`)*. **La corsa:** `mitosi_rami_v2.ciclo` con `nascita_iniziale = False`. **D2, in memoria:** `Campi.residuo` *(entrambi i nomi del modulo `mattone`)* restituisce `max |div E - e (rho - media)|` **senza dividere per `e max rho`**. **(K4)** le nascite spente *(il modo `c2ext`)*, da `35976` a `36250`: `somma |phi_h|^2` e `H` *(la serie `E`)* fra `36000` e `36250` entro `1e-9` relativo.
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
import mitosi_vuoto as MV  # noqa: E402

BASE = MV.BASE
F_VUOTO = MV.F_VUOTO
K0 = MV.K0


def residuo_assoluto(self):
    """### D2: `max |div E - e (rho - media)|`, senza la normalizzazione a `e max rho`; `0` se `e = 0`."""
    import importlib
    MTN = importlib.import_module(type(self).__module__)
    if self.campo is None or self.campo.e == 0.0:
        return 0.0
    rho = MTN.rho_di(self.Z)
    G = self.campo.div() - self.campo.e * (rho - rho.mean())
    return float(np.max(np.abs(G)))


def d2():
    import importlib
    fatti = []
    for nome in ("mattone", "solitone.mattone"):
        try:
            M = importlib.import_module(nome)
        except ImportError:
            continue
        M.Campi.residuo = residuo_assoluto
        fatti.append("%s (%s)" % (nome, M.__file__))
    assert fatti, "nessun modulo mattone da correggere"
    print("### D2: Campi.residuo assoluto in %s" % "; ".join(fatti))


def corsa_v2(modo, fino, d):
    import mitosi_rami_v2 as MR2
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_rami_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "mitosi_vuoto.py"))
    _presidio.avvia(__file__)
    d2()
    assert not glob.glob(os.path.join(d, "stato_*.npz")), "%s ha gia' degli stati: non si riscrive" % d
    os.makedirs(d, exist_ok=True)
    print("### [M0237-4 v2] il vuoto puro, il modo %s, da %s a %d, in %s" % (modo, F_VUOTO, fino, d))
    sys.stdout.flush()
    return MR2.ciclo("vuoto_v2_" + modo, modo, F_VUOTO, fino, None, nascita_iniziale=False, d_out=d)


def noto():
    d = os.path.join(BASE, "vuoto_v2_noto")
    cod, k, _f = corsa_v2("c2ext", 36250, d)
    a, b = np.load(os.path.join(d, "stato_36000.npz")), np.load(os.path.join(d, "stato_36250.npz"))
    na, nb = float(np.sum(np.abs(a["phi_h"]) ** 2)), float(np.sum(np.abs(b["phi_h"]) ** 2))
    with np.load(os.path.join(d, "serie_36250.npz")) as z:
        k_, E = z["k"], z["E"]
    ea, eb = float(E[k_ == 36000][0]), float(E[k_ == 36250][0])
    rn, re = abs(nb / na - 1.0), abs(eb / ea - 1.0)
    ok = cod == 0 and rn < 1e-9 and re < 1e-9
    print("  DEVE: (K4) il vuoto senza nascite (c2ext), 36000 -> 36250: la norma %.12e -> %.12e (%.2e), H %+.12e -> %+.12e (%.2e), entro 1e-9   %s" % (na, nb, rn, ea, eb, re, "PASSA" if ok else "### FALLISCE"))
    return 0 if ok else 1


def lettura():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0237-4 v2] IL VUOTO PURO CON LE NASCITE ACCESE, 6000 TICK, SULLA VIA VERA (la carta doc/CARTA_mitosi.md)")
    print("=" * 130)
    d = os.path.join(BASE, "vuoto_v2")
    ff = sorted(glob.glob(os.path.join(d, "nascite_*.json")))
    b = json.load(open(ff[-1], encoding="utf-8")) if ff else []
    st = sorted(glob.glob(os.path.join(d, "stato_*.npz")))
    print("  gli stati: %d (%s .. %s); le nascite: %d" % (len(st), os.path.basename(st[0]) if st else "-", os.path.basename(st[-1]) if st else "-", len(b)))
    for x in b[:20]:
        print("    k %d: l'arco %s, DH %+.4e" % (int(x["k"]), x["a"], float(x["DH"])))
    print("### NASCITE NEL VUOTO PURO: %s" % ("SI', %d, la prima a k %d" % (len(b), int(b[0]["k"])) if b else "NESSUNA"))
    print("=" * 130)
    return 0


def main(argv):
    os.chdir(os.path.abspath(os.path.join(_QUI, "..", "..")))     # ### dal lanciatore di lapse-u: la radice del worktree mitosi
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa", "lettura"))
    a = ap.parse_args(argv)
    if a.cosa == "corsa":
        cod, k, _f = corsa_v2("mitosi", K0 + 6000, os.path.join(BASE, "vuoto_v2"))
        return cod
    return {"noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
