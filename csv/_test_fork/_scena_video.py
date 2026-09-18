# -*- coding: utf-8 -*-
"""LA SCENA DEL VIDEO, SENZA IL RENDERING -- riproduce `--test N-MASSE` e SALVA lo stato.

⚠ PERCHE' ESISTE, e NON e' una scorciatoia:
  nel ramo headless `--sync-db` **CARICA soltanto** (`:5836-5844`; il commento lo dice:
  *«se --sync-db e il file esiste, CARICA lo stato»*) e **NON CHIAMA MAI `salva_stato`**.
  Quindi il comando del mandato NON produrrebbe nessun `.pkl` e le misure non si potrebbero fare.

NON APPLICO I FLAG A MANO: uso il PERCORSO UFFICIALE del programma, lo stesso di `:7328-7336`
    a = _cli(); _applica_regime(a); _applica_flag(a)
e la scena si avvia col SUO costruttore, `avvia_test("N-MASSE")` -> `_semina_n_masse()`.
Il ciclo per frame e' COPIATO da `update()` (`:5091-5100`), non reinventato:
    passo_test()                                   # una volta per frame: fa avanzare le fasi
    for _ in range(PASSI_PER_FRAME):               # = 6
        scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()

USO:  python _scena_video.py <n_frame> <destinazione> [frame,di,snapshot]
ASCII PURO.
"""
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

_ARGV = list(sys.argv)
NFRAME = int(_ARGV[1]) if len(_ARGV) > 1 else 20
DEST = _ARGV[2] if len(_ARGV) > 2 else os.path.join("csv", "_test_fork", "_gvideo")
SNAP = set(int(x) for x in _ARGV[3].split(",")) if len(_ARGV) > 3 else set()
os.makedirs(DEST, exist_ok=True)

# gli STESSI flag del comando del mandato. `--test` fa scegliere Agg a `:132`: nessuna finestra.
sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "8",
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
            "--viriale", "--olon-part"]
import soliton_simulator as S

print("=" * 112)
print("SCENA DEL VIDEO senza rendering -- %d frame x %d passi = %d passi di motore"
      % (NFRAME, S.PASSI_PER_FRAME, NFRAME * S.PASSI_PER_FRAME))
print("=" * 112)

a = S._cli()                 # IL PERCORSO UFFICIALE: stesso parser del programma
S._applica_regime(a)
S._applica_flag(a)
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None

print("\n  FLAG ATTIVI, letti dal MODULO dopo `_applica_flag` (P6: dai dati, non dal comando):")
for f in ("CAMPO_SPINORIALE", "SPINORE_VIVO", "SPINORE_CORRETTO", "CHI_CORE", "CS_DINAMICO",
          "TAU_LUCE", "CHI_BASC", "FORK_SU2", "FORK_SU2_MEM", "STEP2_OROLOGIO", "SPIN_FEEDBACK",
          "CALORE_VETTORIALE", "PLAST_DIN", "VERLET", "TAU_LOC"):
    print("    %-20s %s" % (f, getattr(S, f, "ASSENTE")))
print("  PASSI_PER_FRAME = %s   DT = %s   TAU_A = %s   N_c(collasso) = %d"
      % (S.PASSI_PER_FRAME, S.DT, S.TAU_A, int(S.massa_critica_collasso())))
print("  ⚠ `--tau-luce` ha il SIGILLO FALLITO (CLAUDE.md par.0): ramo NON CERTIFICATO.")
print("  ⚠ `--chi-basc` RISCRIVE `perc_chi` a ogni passo: non e' un'etichetta di lignaggio.")

S.avvia_test("N-MASSE")()    # il costruttore UFFICIALE della scena -> _semina_n_masse()
print("\n  scena avviata: n = %d nodi alla semina (N_c*0.8 per massa, 3 masse)" % S.net.n)

t0 = time.time()
S.stato["nframe"] = 0
prog = []
for k in range(NFRAME):
    S.passo_test()
    for _ in range(int(S.PASSI_PER_FRAME)):
        S.scuoti_vuoto(S.net); S.net.step(); S.net.mitosi()
        S.net.rilassa_disegno(); S.net.memoria_hebbiana_moto()
    S.stato["nframe"] += 1
    fr = k + 1
    if fr in SNAP or fr == NFRAME:
        S.net._db_step = fr          # ⚠ e' il FRAME, non il passo di motore. DICHIARATO.
        p = os.path.join(DEST, "frame_%d.pkl" % fr)
        S.net.salva_stato(p)
        print("  SNAPSHOT frame %-5d (passi %-6d) n=%-7d -> %s"
              % (fr, fr * S.PASSI_PER_FRAME, S.net.n, p), flush=True)
    if fr % 5 == 0 or fr == 1:
        dg = S.net.diagnostica()
        el = time.time() - t0
        prog.append((fr, S.net.n, el))
        print("  frame %-5d n=%-7d archi=%-8d coer_l=%-8.4g dil=%+7.3f%%   [%.1f s, %.3f s/frame]"
              % (fr, S.net.n, len(S.net.i), dg.get("coer_l", float("nan")),
                 100 * dg.get("dil", float("nan")), el, el / fr), flush=True)

el = time.time() - t0
print("\n  TOTALE %.1f s per %d frame -> %.3f s/frame medio" % (el, NFRAME, el / max(NFRAME, 1)))
if len(prog) >= 2:
    (f1, n1, t1), (f2, n2, t2) = prog[0], prog[-1]
    c1 = t1 / f1; c2 = (t2 - t1) / max(f2 - f1, 1)
    print("  n da %d a %d;  costo per frame da %.3f a %.3f s  (x%.2f)" % (n1, n2, c1, c2, c2 / max(c1, 1e-9)))
    print("  ⚠ IL COSTO CRESCE COL NUMERO DI NODI: un'estrapolazione LINEARE SOTTOSTIMA.")
print("=" * 112)
