# -*- coding: utf-8 -*-
r"""**LE DISTANZE IN FASE: LA COPPIA DI MATTONI DI `L 162` A `50` E A `65` NODI** *(Luca `2026-11-14` `23:32`, L5; `23:50`, la scatola; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `21.5`)*.

    python csv/solitone/coppia_distanze.py --d 50 --registro coppia-d50 > <scratchpad>/coppia_d50.txt     (L 162, il bordo da 60)
    python csv/solitone/coppia_distanze.py --d 65 --registro coppia-d65 > <scratchpad>/coppia_d65.txt     (L 243, il bordo da 100.5: Luca 23:50)

### **`mattone_coppia_L162.main` COSI' COM'E'** *(B2: due mattoni cotti su `L 162`, in fase, G+U, `2000` tick, la lettura)* **con IN MEMORIA:** **(1) un mondo `GUd<d>`** *(i file `coppia_GUd<d>_L162_*`)*; **(2) i due centri:
`carta_coppia.centri_semipiani` alla PRIMA chiamata da' i due punti a `d/2` dal centro del bordo lungo `A1`** *(poi `vicino_mod3` li porta al nodo multiplo di `3`: la distanza VERA stampata)*; **(3) per `d = 65`: la scena di
`L 243`** *(`convergenza.scena_L(243, 100.5)` al posto della scena di C35-pi; `bordo.g_estremita` chiamata col `R_A` di `L 243` invece del `60` di `mattone_coppia_L162`)*: **la scatola DIVERSA, dichiarata** *(Luca
`23:50`: su `L 162` la coda esterna arriverebbe oltre `R_A 60`, una FALSA attrazione)*; **(4) la massa oltre `R_A` dal centro del bordo, all'inizio e alla fine** *(una sottoclasse di `mattone_cottura.Corsa`)*: **deve restare
sotto `1e-4` relativo; se no, scritto accanto alla forza.** **La lettura ATTRAE/RESPINGE: `coppia_fase.py lettura --mondo GUd<d>`.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402

SCATOLA = {50: (162, 60.0), 65: (243, 100.5)}           # ### Luca 23:50: d -> (L, R_A)
SOGLIA_FUORI = 1e-4
FUORI = []
_Corsa = CT.Corsa


def main(argv):
    import _presidio
    import convergenza as CV
    import mattone_coppia_L162 as MCL
    from solitone import bordo as BO
    from solitone import carta_coppia as CC
    from solitone import toro as TO
    for m in ("mattone_coppia_L162", "convergenza", "mattone_cottura", "mattone"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    a = list(argv)
    d = int(a[a.index("--d") + 1])
    resto = a[:a.index("--d")] + a[a.index("--d") + 2:]
    L, R_A = SCATOLA[d]
    mondo = "GUd%d" % d
    MCL.MONDI[mondo] = "MGU"
    # ---------------------------------------------------------------- (3) la scena di L 243 e il suo bordo
    vera_scena, vera_g = MT.scena, BO.g_estremita
    if L == 243:
        def scena(corsa, t):
            return CV.scena_L(243, CV.R_A_243) if corsa == MCL.CORSA_C else vera_scena(corsa, t)
        MT.scena = scena

        def g_estremita(z, c1, c2, R_A_, g_max):
            return vera_g(z, c1, c2, R_A if z["L"] == 243 else R_A_, g_max)
        BO.g_estremita = g_estremita
    # ---------------------------------------------------------------- (2) i due centri alla distanza d
    vero_cs = CC.centri_semipiani
    stato = {"prima": True, "c0": None}

    def centri_semipiani(rho, m1, m2, L_, x, soglia):
        if stato["prima"]:
            stato["prima"] = False
            c0 = stato["c0"]
            A1, A2 = TO.vettori()
            a1 = np.linalg.solve(np.column_stack([A1, A2]), A1 * (d / 2.0))       # ### d/2 lungo A1, in indici
            return np.array([c0[0] - a1[0], c0[1] - a1[1]]), np.array([c0[0] + a1[0], c0[1] + a1[1]])
        return vero_cs(rho, m1, m2, L_, x, soglia)
    CC.centri_semipiani = centri_semipiani

    # ---------------------------------------------------------------- (4) la massa oltre R_A, all'inizio e alla fine
    class CorsaFuori(_Corsa):
        def fuori(self, k):
            Z = self.Z
            rho = MT.rho_di(Z)
            c0 = Z["bordo"]["c0"]
            r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c0[0], c0[1], Z["L"]).T[:2])
            FUORI.append((k, float(rho[r > R_A].sum() / rho.sum())))

        def inizio(self, k):
            _Corsa.inizio(self, k)
            self.fuori(k)

        def passo(self, k, t, r, e):
            _Corsa.passo(self, k, t, r, e)
            if k % 500 == 0:
                self.fuori(k)
    CT.Corsa = CorsaFuori

    vero_scena_ctx = MT.scena

    def scena_col_c0(corsa, t):
        ctx = vero_scena_ctx(corsa, t)
        if corsa != MCL.CORSA_C:
            return ctx

        class Avvolto(object):
            def __enter__(self_):
                Z = ctx.__enter__()
                stato["c0"] = Z["bordo"]["c0"]
                return Z

            def __exit__(self_, *x):
                return ctx.__exit__(*x)
        return Avvolto()
    MT.scena = scena_col_c0
    print("### LE DISTANZE (Luca 23:32, 23:50): d %d su L %d, il bordo da R_A %g; mattone_coppia_L162.main col mondo %s, i centri a d/2 dal centro del bordo lungo A1%s, la massa oltre R_A; SOSTITUITI in memoria"
          % (d, L, R_A, mondo, ", la scena di L 243 (convergenza.scena_L) e bordo.g_estremita col suo R_A" if L == 243 else ""))
    try:
        ok = MCL.main(["--mondo", mondo] + resto)
    finally:
        MT.scena, BO.g_estremita, CC.centri_semipiani, CT.Corsa = vera_scena, vera_g, vero_cs, _Corsa
    print("### LA MASSA OLTRE R_A %g DAL CENTRO DEL BORDO (relativa; la soglia %g): %s" % (R_A, SOGLIA_FUORI, " ".join("k %d %.3e" % x for x in FUORI)))
    peggio = max(x[1] for x in FUORI)
    print("    %s" % ("SOTTO la soglia" if peggio < SOGLIA_FUORI else "### OLTRE la soglia (%.3e): scritto accanto alla forza" % peggio))
    return ok


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
