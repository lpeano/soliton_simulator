# -*- coding: utf-8 -*-
"""RUNNER A SIMULATORE ESPLICITO -- importa UNA copia data del simulatore e ne dumpa lo stato.

Serve al sigillo `V1`: per confrontare DUE versioni del simulatore bisogna poterle caricare
entrambe, e `import soliton_simulator` ne carica una sola, quella della radice. Qui il file si
sceglie con `--sim=<path>` e si carica con `importlib`, cosi' il vecchio si estrae da git in un
percorso qualunque e NON si tocca mai il file della radice.

Uso:  python _runner_sim.py --sim=<path> --out=<npz> [--passi=12]
ASCII PURO.
"""
import importlib.util
import os
import sys

import numpy as np

PASSI = 12
MEDIANA = False
SIM = None
OUT = None
for _x in sys.argv[1:]:
    if _x.startswith("--sim="):
        SIM = os.path.abspath(_x.split("=", 1)[1])
    elif _x.startswith("--out="):
        OUT = os.path.abspath(_x.split("=", 1)[1])
    elif _x.startswith("--passi="):
        PASSI = int(_x.split("=", 1)[1])
    elif _x == "--scala-p-mediana":
        MEDIANA = True
if not SIM or not OUT:
    raise SystemExit("uso: --sim=<path> --out=<npz> [--passi=N]")

# gli STESSI flag del driver, percorso UFFICIALE
sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "8",
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
            "--viriale", "--olon-part"]

_spec = importlib.util.spec_from_file_location("sim_sotto_esame", SIM)
S = importlib.util.module_from_spec(_spec)
sys.modules["sim_sotto_esame"] = S
_spec.loader.exec_module(S)

a = S._cli()
S._applica_regime(a)
S._applica_flag(a)
if MEDIANA:
    # DIAGNOSTICO: la scala VECCHIA, per la riduzione al limite `Y1`. Non c'e' un flag da riga di
    # comando nel simulatore, di proposito: si accende QUI, in processo, e solo il sigillo lo fa.
    if not hasattr(S, "SCALA_P_MEDIANA"):
        raise SystemExit("questo simulatore non ha SCALA_P_MEDIANA: e' la versione PRIMA della cura")
    S.SCALA_P_MEDIANA = True
S._NMASSE_VIDEO["n"] = 3
S._NMASSE_VIDEO["sep"] = 8.0
S._NMASSE_VIDEO["size"] = None
S.avvia_test("N-MASSE")()

for _ in range(PASSI):
    S.scuoti_vuoto(S.net)
    S.net.step()
    S.net.mitosi()
    S.net.rilassa_disegno()
    S.net.memoria_hebbiana_moto()

np.savez(OUT,
         psi=np.asarray(S.net.psi), d=np.asarray(S.net.d), phi=np.asarray(S.net.phi),
         eta=np.asarray(S.net.eta), n=np.asarray([S.net.n]),
         pos=np.asarray(S.net.pos), tw=np.asarray(S.net.tw),
         omega_s=np.asarray(getattr(S.net, "omega_s", np.zeros((1, 3)))),
         mem_mot=np.asarray(getattr(S.net, "mem_mot", np.zeros((1, 3)))))
# i contatori, se il simulatore li ha (V2): si stampano, cosi' il sigillo li legge dallo stdout
if hasattr(S, "rapporto_guardie"):
    r = S.rapporto_guardie(S.net)
    for k in sorted(r):
        v = r[k]
        print("GUARDIA %-14s tot=%-8d salti=%-8d frazione=%-10.6f shape=%-14s quando=%s"
              % (k, v["tot"], v["salti"], v["frazione"], v["shape"], v["quando"]))
else:
    print("GUARDIE: il simulatore %s NON ha rapporto_guardie (e' la versione PRIMA)" % SIM)
# i DIAGNOSTICI della cura di `scala_p` (Y3, Y4) e il momento angolare netto (Y5).
# L e' definito QUI e la definizione si dichiara: L = somma di (pos - baricentro) x mem_mot,
# cioe' il momento angolare della MEMORIA DEL MOTO -- la grandezza su cui agisce L_CONSERVA.
_P = np.asarray(S.net.pos)[:S.net.n]
_M = np.asarray(getattr(S.net, "mem_mot", np.zeros_like(_P)))[:S.net.n]
_L = np.cross(_P - _P.mean(axis=0), _M).sum(axis=0) if len(_P) == len(_M) else np.zeros(3)
print("DIAG amp_med=%.9f sin2_med=%.9f sin2_p95=%.9f Lx=%.6e Ly=%.6e Lz=%.6e |L|=%.6e"
      % (float(getattr(S.net, "_diag_amp_med", float("nan"))),
         float(getattr(S.net, "_diag_sin2_med", float("nan"))),
         float(getattr(S.net, "_diag_sin2_p95", float("nan"))),
         _L[0], _L[1], _L[2], float(np.linalg.norm(_L))))
_nb = getattr(S.net, "_nb", None)
_nbn = (float(np.abs(np.linalg.norm(np.asarray(_nb)[:S.net.n], axis=1) - 1.0).max())
        if _nb is not None and len(_nb) >= S.net.n else float("nan"))
print("STAB nan_psi=%d nan_d=%d nan_pos=%d max||nb|-1|=%.3e"
      % (int(np.sum(~np.isfinite(S.net.psi))), int(np.sum(~np.isfinite(S.net.d))),
         int(np.sum(~np.isfinite(S.net.pos))), _nbn))
print("OK n=%d archi=%d passi=%d" % (S.net.n, len(S.net.i), PASSI))
