# -*- coding: utf-8 -*-
"""`D-b` -- **LA GEOMETRIA DELLA SEMINA: perche' nascono archi sotto `LAM`.**

`_allaccia` prende `dd = M.data` dal `cKDTree`: **la distanza EUCLIDEA VERA fra le posizioni**.
Quindi un arco nasce sotto `LAM` **perche' i due nodi sono stati SEMINATI piu' vicini di
`LAM`** -- `d` non fa altro che riportarlo.

**QUESTA SONDA MISURA LA CAUSA, non il sintomo:** la distribuzione delle distanze al PRIMO
VICINO fra i nodi seminati, contro `LAM` e contro `R_CONN`.

**Serve alla scheda della CURA DELLA SEMINA** *(decisione di Luca, `D-b`)*: una cura si deriva
dai numeri della causa, non dal conteggio del sintomo.

Sola lettura, passo ZERO, un processo. Argv **letta** dal driver.
ASCII puro.
"""
import io
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_revisione", "GEOMETRIA_SEMINA.txt")

FIGLIO = r'''
import os, sys, numpy as np
sys.path.insert(0, os.path.join(RAD, "csv"))
import _testa_driver as T
S, argv, g = T.esegui(os.path.join(RAD, "csv", "_test_fork", "_revisione", "_scarto"), [])
S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
S.avvia_test("N-MASSE")()
net = S.net
from scipy.spatial import cKDTree
pos = np.asarray(net.pos, dtype=float)
LAM = float(S.LAM)
# distanza al PRIMO VICINO di ogni nodo (k=2: il primo e' se stesso)
dist, _ = cKDTree(pos).query(pos, k=2)
nn = np.asarray(dist)[:, 1]
d = np.asarray(net.d, dtype=float)
q = lambda v, p: float(np.percentile(v, p))
print("NN n=%d  LAM=%.6f  R_CONN=%.6f" % (net.n, LAM, float(S.R_CONN())))
print("NN p01=%.6f p10=%.6f p50=%.6f p90=%.6f p99=%.6f min=%.6f max=%.6f"
      % (q(nn,1), q(nn,10), q(nn,50), q(nn,90), q(nn,99), float(nn.min()), float(nn.max())))
print("NN sotto_LAM=%d su %d (%.2f %%)  mediana/LAM=%.6f  min/LAM=%.6f"
      % (int(np.sum(nn < LAM)), nn.size, 100.0*np.sum(nn < LAM)/nn.size,
         q(nn,50)/LAM, float(nn.min())/LAM))
print("ARCHI n=%d  sotto_LAM=%d (%.2f %%)  p50/LAM=%.6f"
      % (d.size, int(np.sum(d < LAM)), 100.0*np.sum(d < LAM)/d.size, q(d,50)/LAM))
# quanti archi RESTEREBBERO se non se ne creassero sotto LAM
print("SE_TAGLIASSI archi_rimasti=%d su %d (%.2f %%)"
      % (int(np.sum(d >= LAM)), d.size, 100.0*np.sum(d >= LAM)/d.size))
# e quanti NODI resterebbero senza NESSUN arco
i = np.asarray(net.i); j = np.asarray(net.j); m = d >= LAM
gr = np.zeros(net.n, int)
np.add.at(gr, i[m], 1); np.add.at(gr, j[m], 1)
print("SE_TAGLIASSI nodi_isolati=%d su %d (%.2f %%)"
      % (int(np.sum(gr == 0)), net.n, 100.0*np.sum(gr == 0)/net.n))
'''


def main():
    try:
        os.makedirs(os.path.dirname(DEST))
    except OSError:
        pass
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    r = subprocess.run([sys.executable, "-c", "RAD = %r\n" % RADICE + FIGLIO],
                       cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    P("# `D-b` -- LA GEOMETRIA DELLA SEMINA: perche' nascono archi sotto `LAM`\n#\n")
    P("# `_allaccia` prende `dd` dal `cKDTree`: la DISTANZA EUCLIDEA VERA fra le posizioni.\n")
    P("# Un arco nasce sotto `LAM` perche' i due nodi sono stati SEMINATI piu' vicini di `LAM`.\n#\n")
    if r.returncode != 0:
        P("*** MORTO (rc=%d) ***\n%s\n" % (r.returncode, (r.stdout + r.stderr)[-2500:]))
        f.close()
        return 1
    for x in (r.stdout or "").splitlines():
        if x.startswith(("NN ", "ARCHI ", "SE_TAGLIASSI ")):
            P("  " + x + "\n")
    P("\n" + "=" * 96 + "\nCOME SI LEGGE\n" + "=" * 96 + "\n")
    P("  `NN` e' la distanza al PRIMO VICINO di ogni nodo: **la piu' corta che quel nodo puo'\n")
    P("  avere**. Se la sua MEDIANA e' sotto `LAM`, allora **la semina mette i nodi piu' fitti\n")
    P("  della lunghezza tipica del sistema**, e nessun aggiustamento sugli ARCHI puo' curarlo:\n")
    P("  il difetto e' nelle POSIZIONI.\n")
    P("\n  `SE_TAGLIASSI` dice cosa costerebbe la cura BANALE -- *non creare archi sotto `LAM`*:\n")
    P("  quanti archi restano e **quanti nodi restano ISOLATI**. Un nodo isolato non e' un nodo\n")
    P("  piu' semplice: **e' un nodo che esce dalla fisica.**\n")
    f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
