# -*- coding: utf-8 -*-
r"""**LA FASE 1 DEL PIANO DI VERIFICA: LE FORZE NELLA SCATOLA GIUSTA** *(Luca `2026-11-16` `17:47`; il piano `doc/PIANO_VERIFICA_SCATOLA.md`)*.

    E:\python\py3132\python.exe csv/solitone/verifica_coppie.py --d 35 --L 297 --fase 0 --registro verifica-F35 > <scratchpad>/verifica_F35.txt
    (F-35, F-51 su L 351, F-66 su L 402; A-35 --fase pi su L 297, A-45 su L 330, A-51 su L 351, A-66 su L 402)

### **`mattone_coppia_L162.main` COSI' COM'E'** *(B2: due mattoni cotti su `L 162`, G+U, `2000` tick, la lettura B3)*, **con IN MEMORIA, come `coppia_distanze.py` e `coppia_fase.py`** *(che non si toccano)*:
**(1) un mondo `V<L>d<d>` o `V<L>d<d>pi`** *(i file `coppia_<mondo>_L162_*`: il suffisso `L162` e' del codice di `mattone_coppia_L162`, la scena e' `L`)*; **(2) la scena `convergenza.scena_L(L, R_A)` col bordo da
`R_A = d + 50`** *(`2 R_ogg`, con `R_ogg = d/2 + 25`: il piano)*; **(3) i due centri a `d/2` dal centro del bordo lungo `A1`; (4) per `pi`: il francobollo B con `psi -> -psi`; (5) la massa oltre `R_A` dal centro del
bordo, all'inizio e ogni `500`; (6) LA REGOLA R-SCATOLA AL 5%, A TRE CLAUSOLE, sulla coppia appena incollata** *(`R_ogg` misurato al `5%` attorno al baricentro di `rho`: se una clausola cade, la corsa si FERMA)*;
**(7) le tappe nel registro del PRINCIPALE** *(`_registro_corse.tappa`, non quello del mattone: la nave e' chiusa)*.
"""
import argparse
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

SOGLIA_FUORI = 1e-4
FUORI = []
_Corsa = CT.Corsa


class FermoScatola(Exception):
    pass


def main(argv):
    import _presidio
    import convergenza as CV
    import mattone_coppia_L162 as MCL
    import prova_scatola5 as PS5
    from solitone import _registro_corse as RC
    from solitone import bordo as BO
    from solitone import carta_coppia as CC
    from solitone import toro as TO
    for m in ("mattone_coppia_L162", "convergenza", "mattone_cottura", "mattone", "prova_scatola5"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--d", type=float, required=True)
    ap.add_argument("--L", type=int, required=True)
    ap.add_argument("--fase", required=True, choices=("0", "pi"))
    x, resto = ap.parse_known_args(argv)
    d, L, pi = x.d, x.L, x.fase == "pi"
    R_A = d + 50.0
    mondo = "V%dd%d%s" % (L, int(round(d)), "pi" if pi else "")
    MCL.MONDI[mondo] = "MGU"
    salvati = (MT.scena, BO.g_estremita, CC.centri_semipiani, CT.Corsa, MT.incolla, MT.tappa)
    # ---------------------------------------------------------------- (2) la scena di L e il suo bordo
    vera_scena, vera_g = MT.scena, BO.g_estremita
    stato = {"prima": True, "c0": None, "incollature": 0}

    def scena(corsa, t):
        if corsa != MCL.CORSA_C:
            return vera_scena(corsa, t)
        ctx = CV.scena_L(L, R_A)

        class Avvolto(object):
            def __enter__(self_):
                Z = ctx.__enter__()
                stato["c0"] = Z["bordo"]["c0"]
                return Z

            def __exit__(self_, *a):
                return ctx.__exit__(*a)
        return Avvolto()
    MT.scena = scena

    def g_estremita(z, c1, c2, R_A_, g_max):
        return vera_g(z, c1, c2, R_A if z["L"] == L else R_A_, g_max)
    BO.g_estremita = g_estremita
    # ---------------------------------------------------------------- (3) i due centri alla distanza d
    vero_cs = CC.centri_semipiani

    def centri_semipiani(rho, m1, m2, L_, xx, soglia):
        if stato["prima"]:
            stato["prima"] = False
            c0 = stato["c0"]
            A1, A2 = TO.vettori()
            a1 = np.linalg.solve(np.column_stack([A1, A2]), A1 * (d / 2.0))
            return np.array([c0[0] - a1[0], c0[1] - a1[1]]), np.array([c0[0] + a1[0], c0[1] + a1[1]])
        return vero_cs(rho, m1, m2, L_, xx, soglia)
    CC.centri_semipiani = centri_semipiani
    # ---------------------------------------------------------------- (4) l'antifase: il francobollo B con psi -> -psi
    vero_inc = MT.incolla

    def incolla(Z, fr, c, allinea):
        stato["incollature"] += 1
        if pi and stato["incollature"] == 2:
            fr = dict(fr)
            fr["psi"] = -fr["psi"]
        return vero_inc(Z, fr, c, allinea)
    MT.incolla = incolla

    # ---------------------------------------------------------------- (5) la massa oltre R_A; (6) la regola al 5% all'inizio
    class CorsaVerifica(_Corsa):
        def fuori(self, k):
            Z = self.Z
            rho = MT.rho_di(Z)
            c0 = Z["bordo"]["c0"]
            r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c0[0], c0[1], Z["L"]).T[:2])
            FUORI.append((k, float(rho[r > R_A].sum() / rho.sum())))

        def inizio(self, k):
            _Corsa.inizio(self, k)
            self.fuori(k)
            Z = self.Z
            if Z["L"] == L and "regola_fatta" not in stato:
                stato["regola_fatta"] = True
                Rm, rr, b = PS5.r5(Z, MT.G2.T0 + k)
                print("### la coppia incollata: i raggi %s attorno al baricentro (%.2f, %.2f); R_ogg al 5%% %.1f (il piano: d/2 + 25 = %.1f)"
                      % (", ".join("%g%% %s" % (100 * s, rr[s]) for s in sorted(rr, reverse=True)), b[0], b[1], Rm, d / 2.0 + 25.0))
                if not PS5.regola(Z, Rm, "la coppia a k %d" % k):
                    raise FermoScatola("R-SCATOLA al 5% NON rispettata sulla coppia: la corsa NON parte (il piano)")

        def passo(self, k, t, r, e):
            _Corsa.passo(self, k, t, r, e)
            if k % 500 == 0:
                self.fuori(k)
    CT.Corsa = CorsaVerifica
    # ---------------------------------------------------------------- (7) le tappe nel registro del principale
    MT.tappa = lambda nome, testo: RC.tappa(nome, testo) if nome else None
    print("### LA FASE 1 DEL PIANO DI VERIFICA (Luca 17:47): d %g, fase %s, L %d, il bordo da R_A %g; mattone_coppia_L162.main col mondo %s; la scena convergenza.scena_L, i centri a d/2 lungo A1%s, la massa oltre R_A, la regola al 5%%, le tappe nel registro del principale; SOSTITUITI in memoria"
          % (d, x.fase, L, R_A, mondo, ", il francobollo B con psi -> -psi" if pi else ""))
    sys.stdout.flush()
    try:
        ok = MCL.main(["--mondo", mondo] + resto)
    except FermoScatola as z:
        print("### FERMO: %s" % z)
        ok = 1
    finally:
        MT.scena, BO.g_estremita, CC.centri_semipiani, CT.Corsa, MT.incolla, MT.tappa = salvati
    print("### le incollature: %d (attese 2%s)" % (stato["incollature"], ": A, poi B girato" if pi else ""))
    print("### LA MASSA OLTRE R_A %g DAL CENTRO DEL BORDO (relativa; la soglia %g): %s" % (R_A, SOGLIA_FUORI, " ".join("k %d %.3e" % y for y in FUORI)))
    if FUORI:
        peggio = max(y[1] for y in FUORI)
        print("    %s" % ("SOTTO la soglia" if peggio < SOGLIA_FUORI else "### OLTRE la soglia (%.3e): scritto accanto alla forza" % peggio))
    return ok


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
