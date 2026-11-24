# -*- coding: utf-8 -*-
r"""**[M1631] IL TORNEO DELLE FORME: LE TENUTE (5a)** *(il passo 4 del torneo; la carta `doc/CARTA_torneo_nonlinearita.md`, sez. `7` e `10`; il task history `doc/TASK_HISTORY/2026-11-22_torneo_lanciatori.md`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/torneo_tenuta.py controlli > doc/referti_l2/torneo_controlli.txt
    E:\python\py3132\python.exe doc/referti_l2/torneo_tenuta.py corsa --forma FH --semina cima --fino 3000
    E:\python\py3132\python.exe doc/referti_l2/torneo_tenuta.py lettura > doc/referti_l2/torneo_tenuta.txt

**La scena e il tick:** V0 della caduta libera *(`caduta_libera.prepara`; `caduta_segno_v2.tick_var` con `N = 1`, `cs = s`, senza la fase (a); il `residuo` di Gauss come in `caduta_libera.corsa`)*; ### **dentro la scena i `pezzi` del NUCLEO** *(`ripresa_F0_v2.col_nucleo`)* **e la forma con `materia_vuoto.forma_esplicita`**. **Gli stati** ogni `250` in `E:\soliton_simulator\controllo\M1631\tenuta\<forma>_<semina>`. ### ⛔ **La semina al FONDO non c'e' ancora:** la portante non e' definita *(la banda piu' bassa e' degenere: `doc/referti_l2/torneo_fondo_v2.txt`)*, e la scelta e' di Luca: `--semina` diverso da `cima` ALZA.

**`controlli`** *(K1 del lanciatore, la carta sez. 10)*: **(1)** `lambda = 1` costruita in memoria *(`MV._forma_lambda(1.0)` al posto di `MV.alpha`, `MV.beta`)* **= S1 AL BIT**, lo sha1 dello stato a `100` tick con la materia; **(2)** **il vuoto da solo** *(`MT.vuoto_fresco`, il campo di `PO.campi`)* **a `100` tick con ogni forma = S1 AL BIT**; **(3)** **ogni forma diversa da S1 cambia lo stato con la materia dopo UN tick** *(il caso che DEVE differire: la forma si legge)*; **(4)** il percorso del nucleo a S1 = quello di `csv/` della scena, UN tick, al bit.

**`lettura`** *(la carta sez. 10: K-T)*: per ogni corsa a `k 500` e `k 3000`: la densita' per nodo lisciata *(la media sui `7` nodi del vicinato)*; **`w = sqrt(A_half/pi)`**, `A_half` = i nodi sopra meta' del massimo lisciato per `sqrt(3)/2`; **i pezzi:** le componenti connesse *(i `6` vicini, sul toro)* dei nodi sopra il `10%` del massimo lisciato. **K-T:** `w(3000)/w(500)` entro `[0.7, 1.3]` **e** un solo pezzo a `k 3000`. **I casi noti:** F0 alla cima DEVE reggere *(se non regge, il criterio e' rotto: lo dico per primo)*.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import ripresa_F0_v2 as RF  # noqa: E402

DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1631", "tenuta")
OGNI_STATO = 250
FORME_TORNEO = ("L+0.5", "L+0.25", "L0", "L-0.25", "L-0.5", "L-1", "FH", "FT")
VICINI = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1))
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append(bool(ok))
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def avvia():
    import _presidio
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "triangolo_chi_v4.py", "ripresa_F0_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def nucleo():
    """### `(MV, pezzi del NUCLEO)`, presi PRIMA della scena *(l'assert sul file)*."""
    import materia_vuoto as MV
    P = MV.pezzi
    assert P.__module__ == "materia_vuoto" and P.__code__.co_filename == os.path.abspath(MV.__file__), "pezzi NON e' quello del nucleo: FERMO"
    return MV, P


def impronta(Z, C):
    h = hashlib.sha1()
    for x in Z["chiavi"]:
        h.update(np.ascontiguousarray(Z["st"][x]).tobytes())
    for a in (C.campo.A, C.campo.E):
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


def corsa(forma, semina, k_fino):
    avvia()
    assert semina == "cima", "la semina %r NON e' definita: la portante al fondo e' una decisione di Luca (doc/referti_l2/torneo_fondo_v2.txt)" % semina
    MV, P0 = nucleo()
    assert forma in MV.FORME, "la forma %r non e' nel nucleo %s" % (forma, sorted(MV.FORME))
    _G20, _ia, e0, MT = CL.parametri()
    nome = "%s_%s" % (forma, semina)
    d_out = os.path.join(DIR, nome)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        C, info = CL.prepara(Z)
        s = float(Z["s"])
        N = np.ones(Z["mot"].inc.n)
        meta = dict(info, forma=forma, semina=semina, s=s, e0=e0)
        print("### %s: la forma %s, la semina %s; il centro %s; s %r, e0 %r; l'impronta di partenza %s; gli stati in %s" % (nome, forma, semina, info["centro"], s, e0, impronta(Z, C), d_out))
        sys.stdout.flush()

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            h = hashlib.sha1(open(fz, "rb").read()).hexdigest()
            open(fz + ".sha1", "w", encoding="utf-8").write(h + "\n")
            return h

        print("    [stato] k 0 sha1 %s" % salva(0)[:8])
        t1 = time.time()
        with RF.col_nucleo(MV, P0), MV.forma_esplicita(forma):
            assert MV.ATTIVA == forma and MV.pezzi is P0
            for k in range(1, k_fino + 1):
                CS.tick_var(Z["z"], C.campo, s, e0, N, False, 0)
                if k % MT.OGNI_GAUSS == 0:
                    C.residuo()
                if k % OGNI_STATO == 0 or k == k_fino:
                    print("    [stato] k %d sha1 %s  (%.0f s)" % (k, salva(k)[:8], time.time() - t1))
                    sys.stdout.flush()
        Z["metti"]()
    print("### %d tick in %.0f s (%.3f s per tick)" % (k_fino, time.time() - t1, (time.time() - t1) / k_fino))
    return 0


def controlli():
    import _u1_prototipo as U1
    avvia()
    MV, P0 = nucleo()
    _G20, _ia, e0, MT = CL.parametri()
    PO = TC.moduli()[5]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    print("=" * 130)
    print("[M1631] I CONTROLLI K1 DEL LANCIATORE (la carta sez. 10): la forma della tabella %s; le forme del nucleo %s" % (MV.ATTIVA, sorted(MV.FORME)))
    print("=" * 130)
    with TC.scena() as Z:
        mot = Z["mot"]
        n = mot.inc.n
        s = float(Z["s"])
        N = np.ones(n)
        C, _info = CL.prepara(Z)
        X0 = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy())

        def rimetti(X):
            Z["metti"](X[0])
            C.campo.A[...] = X[1]
            C.campo.E[...] = X[2]
            U1.scrivi_U(mot, C.campo)

        def gira(X, quanti, forma=None, lam1=False, nucleo_=True):
            rimetti(X)
            a0, b0 = MV.alpha, MV.beta
            ctx = RF.col_nucleo(MV, P0) if nucleo_ else __import__("contextlib").nullcontext()
            with ctx, (MV.forma_esplicita(forma) if forma else __import__("contextlib").nullcontext()):
                if lam1:
                    _n, MV.alpha, MV.beta = MV._forma_lambda(1.0)
                try:
                    for k in range(1, quanti + 1):
                        CS.tick_var(Z["z"], C.campo, s, e0, N, False, 0)
                        if k % MT.OGNI_GAUSS == 0:
                            C.residuo()
                finally:
                    MV.alpha, MV.beta = a0, b0
            return impronta(Z, C)

        # ### (4) il percorso del nucleo a S1 = quello di csv/, UN tick
        h_csv = gira(X0, 1, nucleo_=False)
        h_nuc = gira(X0, 1, "S1")
        esito("(4) UN tick: il percorso del nucleo a S1 = quello di csv/ della scena, al bit", h_csv == h_nuc, "%s %s" % (h_csv[:8], h_nuc[:8]))
        # ### (3) ogni forma diversa da S1 cambia lo stato con la materia dopo UN tick
        for f in FORME_TORNEO:
            h = gira(X0, 1, f)
            esito("(3) ### DEVE differire: UN tick con la materia, %s contro S1" % f, h != h_nuc, h[:8])
        # ### (1) lambda = 1 in memoria = S1, 100 tick con la materia
        h_s1 = gira(X0, 100, "S1")
        h_l1 = gira(X0, 100, "S1", lam1=True)
        esito("(1) lambda = 1 (in memoria) = S1 AL BIT, 100 tick con la materia", h_l1 == h_s1, "%s %s" % (h_l1[:8], h_s1[:8]))
        # ### (2) il vuoto da solo, 100 tick, ogni forma = S1
        Z["metti"]()
        Z["g_e"] = np.zeros_like(Z["g_e"])
        MT.vuoto_fresco(Z, t0)
        Cv = PO.campi(Z, rho_c, e)
        C.campo.A[...] = Cv.campo.A
        C.campo.E[...] = Cv.campo.E
        Xv = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy())
        print("  il vuoto da solo: max |psi_h| %.1e (DEVE essere 0)" % float(np.max(np.abs(Xv[0]["psi_h"]))))
        esito("(2) il vuoto da solo ha psi = 0", float(np.max(np.abs(Xv[0]["psi_h"]))) == 0.0)
        hv = gira(Xv, 100, "S1")
        for f in FORME_TORNEO:
            h = gira(Xv, 100, f)
            esito("(2) il vuoto da solo, 100 tick: %s = S1 AL BIT" % f, h == hv, "%s %s" % (h[:8], hv[:8]))
        h_vcsv = gira(Xv, 100, nucleo_=False)
        esito("(2) il vuoto da solo, 100 tick: il nucleo a S1 = csv/ della scena, al bit", h_vcsv == hv, "%s" % h_vcsv[:8])
        Z["metti"]()
    print("=" * 130)
    print("  %d DEVE su %d   %s" % (sum(ESITI), len(ESITI), "TUTTI PASSATI" if all(ESITI) else "### CI SONO BUCHI"))
    print("=" * 130)
    return 0 if all(ESITI) else 1


def lisciata(rho, L):
    g = rho.reshape(L, L)
    return ((g + sum(np.roll(np.roll(g, a, 0), b, 1) for a, b in VICINI)) / 7.0).reshape(-1)


def pezzi(sopra, L):
    """### Le componenti connesse dei nodi `sopra` *(i `6` vicini, sul toro)*: la propagazione dell'etichetta minima fino al punto fisso."""
    g = sopra.reshape(L, L)
    big = L * L + 1
    lab = np.where(g, np.arange(L * L).reshape(L, L), big)
    while True:
        m = lab.copy()
        for a, b in VICINI:
            m = np.minimum(m, np.where(g, np.roll(np.roll(lab, a, 0), b, 1), big))
        m = np.where(g, m, big)
        if np.array_equal(m, lab):
            break
        lab = m
    return len(np.unique(lab[g]))


def misura(f, nodo, n, L):
    import gravita_due_corpi_misure as GM
    X, _m = GM.leggi(f)
    rho = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
    lis = lisciata(rho, L)
    mx = float(lis.max())
    w = math.sqrt(float(np.sum(lis > 0.5 * mx)) * math.sqrt(3.0) / 2.0 / math.pi)
    return w, pezzi(lis > 0.1 * mx, L), mx, float(rho.sum())


def lettura():
    avvia()
    print("=" * 130)
    print("[M1631] LE TENUTE (5a; la carta sez. 7 e 10): K-T = w(3000)/w(500) entro [0.7, 1.3] e un solo pezzo a k 3000")
    print("=" * 130)
    with TC.scena() as Z:
        nodo = np.asarray(Z["mot"].inc.nodo)
        n, L = Z["n"], Z["L"]
        Z["metti"]()
    tab = {}
    for nome in sorted(os.listdir(DIR)) if os.path.isdir(DIR) else []:
        d = os.path.join(DIR, nome)
        f5, f30 = os.path.join(d, "stato_000500.npz"), os.path.join(d, "stato_003000.npz")
        if not (os.path.exists(f5) and os.path.exists(f30)):
            print("  %-14s ### non finita (manca k 500 o k 3000)" % nome)
            continue
        w5, p5, m5, M5 = misura(f5, nodo, n, L)
        w30, p30, m30, M30 = misura(f30, nodo, n, L)
        r = w30 / w5
        regge = 0.7 <= r <= 1.3 and p30 == 1
        tab[nome] = regge
        print("  %-14s w %.3f -> %.3f (il rapporto %.3f); i pezzi %d -> %d; il picco lisciato %.4e -> %.4e; la massa %.6f -> %.6f: %s" % (
            nome, w5, w30, r, p5, p30, m5, m30, M5, M30, "REGGE" if regge else "### NON REGGE"))
    print("-" * 130)
    if "S1_cima" in tab:
        esito("il caso noto: F0 (S1) alla cima REGGE (se no, il criterio e' rotto)", tab["S1_cima"])
    print("=" * 130)
    return 0 if all(ESITI) else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("corsa", "controlli", "lettura"))
    ap.add_argument("--forma")
    ap.add_argument("--semina", default="cima")
    ap.add_argument("--fino", type=int, default=3000)
    a = ap.parse_args(argv)
    if a.cosa == "corsa":
        return corsa(a.forma, a.semina, a.fino)
    if a.cosa == "controlli":
        return controlli()
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
