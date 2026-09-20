# -*- coding: utf-8 -*-
"""SIGILLO DELLA CURA DI `scala_p` -- Y0-Y8.

Mandato: doc/TASK_HISTORY/2026-09-20_scala-p-punto-fisso.md (f90fc1b).

TRE BRACCI, in processi separati (`_runner_sim.py`, importlib: il file della radice non si tocca):
  A  simulatore PRIMA della cura (estratto da git IN BINARIO)          -> la scala VECCHIA
  B  simulatore ORA, con `SCALA_P_MEDIANA = True`                      -> la scala VECCHIA, forzata
  C  simulatore ORA, default                                           -> LA CURA

  Y1  RIDUZIONE AL LIMITE [BLOCCANTE]:  A == B, BYTE-IDENTICO su psi, d, phi, eta, n, pos, tw.
      Se la forma algebrica non fosse esatta, qui si vedrebbe (lezione R1).
  Y2  CONTROLLO POSITIVO:               A != C. Senza, la cura potrebbe essere inerte.
  Y3  IL PUNTO FISSO E' SCIOLTO:        `median(ampiezza)` vale tanh(1) in B e NON in C.
      Misurato SUL PERCORSO VERO (`_diag_amp_med`), non in una replica.
  Y4  LA RIPARTIZIONE SI MUOVE:         `sin2` mediana e p95, B contro C.
  Y5  L'EFFETTO SU `L`:                 il momento angolare netto, B contro C.
  Y6  `ZETA_VIR` EREDITA:               il moltiplicatore di `beta` E' `(1 - sin2)`: si riporta.
  Y7  STABILITA':                       niente NaN, `|nb| = 1`.
  Y8  si rigirano gli altri sigilli del giro (a parte, non qui).

ASCII PURO.
"""
import os
import re
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM_ORA = os.path.join(RADICE, "soliton_simulator.py")
BASE = os.path.join(RADICE, "csv", "_seal_fork", "_sig_scala_p")
COMMIT_PRIMA = "b9a546d"        # l'ultimo commit PRIMA della cura (contatori gia' dentro)
PASSI = 12
CAMPI = ("psi", "d", "phi", "eta", "n", "pos", "tw")
TANH1 = float(np.tanh(1.0))

esiti = []


def segna(nome, ok, det):
    esiti.append((nome, ok))
    print("%-5s %-6s %s" % (nome, "PASS" if ok else "FAIL", det))


def gira(sim, out, extra=()):
    cmd = [sys.executable, os.path.join(_QUI, "_runner_sim.py"),
           "--sim=%s" % sim, "--out=%s" % out, "--passi=%d" % PASSI] + list(extra)
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:])
        print(pr.stderr[-2000:])
        raise SystemExit("runner uscito con %d" % pr.returncode)
    return pr.stdout


def diag(out):
    m = re.search(r"DIAG amp_med=(\S+) sin2_med=(\S+) sin2_p95=(\S+) "
                  r"Lx=(\S+) Ly=(\S+) Lz=(\S+) \|L\|=(\S+)", out)
    if not m:
        return None
    k = [float(x) for x in m.groups()]
    return dict(amp=k[0], s2med=k[1], s2p95=k[2], L=np.array(k[3:6]), Lmod=k[6])


def confronta(a, b):
    fuori = []
    for k in CAMPI:
        x, y = a[k], b[k]
        if x.shape != y.shape:
            fuori.append("%s(shape %s vs %s)" % (k, x.shape, y.shape))
        elif not np.array_equal(x, y):
            fuori.append("%s(max|A-B|=%.3e)"
                         % (k, float(np.nanmax(np.abs(np.asarray(x, float) - np.asarray(y, float))))))
    return fuori


def main():
    os.makedirs(BASE, exist_ok=True)
    import hashlib
    vecchio = os.path.join(BASE, "_sim_prima.py")
    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    with open(vecchio, "wb") as f:
        f.write(q.stdout)
    with open(SIM_ORA, "rb") as f:
        dn = f.read()
    print("Y0  simulatore PRIMA (%s): sha1 grezzo %s" % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    print("Y0  simulatore ORA            : sha1 grezzo %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("")

    oA, oB, oC = (os.path.join(BASE, x) for x in ("A.npz", "B.npz", "C.npz"))
    print("braccio A: PRIMA della cura, default")
    outA = gira(vecchio, oA)
    print("braccio B: ORA, SCALA_P_MEDIANA=True (la scala vecchia, FORZATA)")
    outB = gira(SIM_ORA, oB, ["--scala-p-mediana"])
    print("braccio C: ORA, default (LA CURA)")
    outC = gira(SIM_ORA, oC)
    print("")
    A, B, C = np.load(oA), np.load(oB), np.load(oC)
    dA, dB, dC = diag(outA), diag(outB), diag(outC)

    # ---------------------------------------------------------------- Y1
    f1 = confronta(A, B)
    segna("Y1", not f1,
          "riduzione al limite A==B su %d campi: %s"
          % (len(CAMPI), "BYTE-IDENTICI" if not f1 else "DIVERSI -> %s" % f1))
    if f1:
        print("  *** Y1 e' BLOCCANTE: la forma algebrica NON e' esatta. Si riscrive, non si allenta. ***")
        return 1

    # ---------------------------------------------------------------- Y2
    f2 = confronta(A, C)
    segna("Y2", len(f2) > 0,
          "controllo positivo A!=C: %d campi su %d differiscono -> la cura FA QUALCOSA"
          % (len(f2), len(CAMPI)))

    # ---------------------------------------------------------------- Y3
    if dB is None or dC is None:
        segna("Y3", False, "diagnostici assenti")
    else:
        okB = abs(dB["amp"] - TANH1) < 1e-9
        okC = abs(dC["amp"] - TANH1) > 1e-6
        segna("Y3", okB and okC,
              "median(ampiezza):  scala VECCHIA %.9f (tanh(1) = %.9f)   CURATA %.9f   -> %s"
              % (dB["amp"], TANH1, dC["amp"],
                 "PUNTO FISSO SCIOLTO" if (okB and okC) else "NON sciolto"))

    # ---------------------------------------------------------------- Y4 e Y6
    if dB and dC:
        segna("Y4", abs(dC["s2med"] - dB["s2med"]) > 1e-9 or abs(dC["s2p95"] - dB["s2p95"]) > 1e-9,
              "sin2  mediana %.6f -> %.6f    p95 %.6f -> %.6f"
              % (dB["s2med"], dC["s2med"], dB["s2p95"], dC["s2p95"]))
        print("Y6         il moltiplicatore di beta E' (1 - sin2):  mediana %.6f -> %.6f  (%+.2f %%)"
              % (1 - dB["s2med"], 1 - dC["s2med"],
                 100.0 * ((1 - dC["s2med"]) / max(1 - dB["s2med"], 1e-12) - 1.0)))
        # ------------------------------------------------------------ Y5
        print("Y5         L (somma di (pos-baricentro) x mem_mot, definizione DICHIARATA):")
        print("             scala VECCHIA  [%11.4e %11.4e %11.4e]  |L| = %.6e"
              % (dB["L"][0], dB["L"][1], dB["L"][2], dB["Lmod"]))
        print("             CURATA         [%11.4e %11.4e %11.4e]  |L| = %.6e"
              % (dC["L"][0], dC["L"][1], dC["L"][2], dC["Lmod"]))
        if dB["Lmod"] > 0:
            print("             |L| CURATA / |L| VECCHIA = %.4f" % (dC["Lmod"] / dB["Lmod"]))

    # ---------------------------------------------------------------- Y7
    m = re.search(r"STAB nan_psi=(\d+) nan_d=(\d+) nan_pos=(\d+) max\|\|nb\|-1\|=(\S+)", outC)
    if m:
        nps, nd, npo, nb = int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4))
        segna("Y7", nps == 0 and nd == 0 and npo == 0 and nb < 1e-9,
              "stabilita': nan psi/d/pos = %d/%d/%d   max||nb|-1| = %.3e" % (nps, nd, npo, nb))
    else:
        segna("Y7", False, "riga STAB assente")

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    if n_pass == len(esiti):
        print("VERDETTO: la cura RIDUCE ESATTAMENTE alla vecchia scala quando la si forza, FA")
        print("  QUALCOSA quando non la si forza, e SCIOGLIE il punto fisso di median(ampiezza).")
    else:
        print("VERDETTO: IL SIGILLO NON PASSA. La cura NON si usa.")
    print("NB: UNA scena, UN seme, %d passi. Y5 e Y6 sono MISURE, non verdetti di fisica." % PASSI)
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
