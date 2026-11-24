# -*- coding: utf-8 -*-
r"""**[M1631] LA RIPRESA DI UNO STATO DI OGGI, AL BIT -- v2** *(la v1, `ripresa_F0.py` 44d8a450, falli' due DEVE: `doc/referti_l2/ripresa_F0_prima.txt`; i due errori della v1 sotto)* *(il passo 3 del torneo: il braccio 0 PRIMA del nucleo, la prova DOPO; `doc/TASK_HISTORY/2026-11-22_torneo_nucleo.md`, R0 e R3)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/ripresa_F0_v2.py --nome prima > doc/referti_l2/ripresa_F0_v2_prima.txt
    E:\python\py3132\python.exe doc/referti_l2/ripresa_F0_v2.py --nome dopo  > doc/referti_l2/ripresa_F0_v2_dopo.txt

**Lo stato `CHI/caduta/V1/stato_001750.npz`** *(la caduta libera di oggi, V1: `chi` acceso, `cs = s N`, la fase (a) `+1`)*, **il campo `A` ed `E` dal file, `N` dal file**; **`250` tick di `caduta_segno_v2.tick_var`** col `residuo` di Gauss allo stesso `k` assoluto della corsa *(`caduta_libera.corsa`; il residuo si legge e basta)*; **lo stato a `k 2000` contro `stato_002000.npz` del disco, ARRAY PER ARRAY, AL BIT** *(ogni chiave dello stato, `campo_A`, `campo_E`)*. **I due controlli che DEVONO fallire:** lo stato a `k 1999` NON e' quello del file a `k 2000`; **UN tick con la forma `S3`** *(`materia_vuoto.forma_esplicita`)* **NON e' UN tick con la forma della tabella** *(la forma si legge davvero)*. **La forma della tabella si stampa** *(`MV.ATTIVA`)*: **deve essere `S1`.**

### **I DUE ERRORI DELLA v1, e le cure:** **(1)** `mattone.scena` tiene la scena intera dentro `_screening_forme_s3.forma(VC.FORMA)`, che SOSTITUISCE `materia_vuoto.pezzi` con le espressioni S1 di `csv/` *(`pezzi_di("S1")`, che non chiama `MV.alpha`/`MV.beta`)*: **`forma_esplicita` del nucleo non arriva al tick.** **Cura:** `pezzi` del NUCLEO si prende all'import *(prima della scena)* e, per i controlli della forma, si rimette dentro la scena *(`col_nucleo`)*; **e un DEVE nuovo: UN tick col percorso di `csv/` (S1) = UN tick col percorso del nucleo (S1), AL BIT** *(cio' che i lanciatori del torneo useranno)*. **(2)** `Z["metti"]` rimette `mot.geo.U = I`, e la v1 non riscriveva `U` dal campo: **la prima meta' del tick 1751 girava con `U = I`** *(nella corsa `U` viene da `A`: `PO.campi` e `_u1_prototipo.avvolto` chiamano `scrivi_U`)*. **Cura:** `rimetti` chiama `_u1_prototipo.scrivi_U(mot, campo)`. **E la ripresa gira PER PRIMA**, prima di ogni tick di controllo.
"""
import argparse
import hashlib
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_libera as CL  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402
import gravita_due_corpi_misure as GM  # noqa: E402

K_DA, K_A = 1750, 2000


@__import__("contextlib").contextmanager
def col_nucleo(MV, P_nucleo):
    """### dentro la scena: `MV.pezzi` = quello del NUCLEO *(non quello di `csv/` della scena)*, rimesso all'uscita."""
    vero = MV.pezzi
    MV.pezzi = P_nucleo
    try:
        yield
    finally:
        MV.pezzi = vero


def main(argv):
    import _presidio
    import materia_vuoto as MV
    import _u1_prototipo as U1
    P_nucleo = MV.pezzi
    assert P_nucleo.__module__ == "materia_vuoto" and P_nucleo.__code__.co_filename == os.path.abspath(MV.__file__), "pezzi all'import NON e' quello del nucleo: FERMO"
    ap = argparse.ArgumentParser()
    ap.add_argument("--nome", required=True)
    a = ap.parse_args(argv)
    for m in ("caduta_libera.py", "caduta_segno_v2.py", "triangolo_chi_v4.py", "gravita_due_corpi_misure.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    d = os.path.join(CL.BASE, "V1")
    X0, m0 = GM.leggi(os.path.join(d, "stato_%06d.npz" % K_DA))
    X1, m1 = GM.leggi(os.path.join(d, "stato_%06d.npz" % K_A))
    acceso, cs_N, segno, _sc = CL.VARIANTI["V1"]
    _G20, _ia, e0, MT = CL.parametri()
    print("=" * 130)
    print("[M1631] LA RIPRESA AL BIT (%s): CHI/caduta/V1 da k %d a k %d; la forma della tabella %s; cs %s, la fase (a) %+d; e0 %r (il file %r)" % (
        a.nome, K_DA, K_A, MV.ATTIVA, "s N" if cs_N else "s", segno, e0, m0["e0"]))
    print("=" * 130)
    ok = []

    def esito(che, passa, nota=""):
        ok.append(bool(passa))
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if passa else "### FALLISCE", nota))
        sys.stdout.flush()

    esito("la forma della tabella e' S1 (F0)", MV.ATTIVA == "S1", MV.ATTIVA)
    esito("e0 della corsa = e0 di oggi", float(m0["e0"]) == e0)
    chiavi_campo = ("campo_A", "campo_E")
    with TC.scena() as Z:
        C, _info = CL.prepara(Z)
        s = float(Z["s"])
        esito("s della corsa = s di oggi", float(m0["s"]) == s)
        N = X0["N"]

        def rimetti():
            Z["metti"]({x: X0[x] for x in Z["chiavi"]})
            C.campo.A[...] = X0["campo_A"]
            C.campo.E[...] = X0["campo_E"]
            U1.scrivi_U(Z["mot"], C.campo)

        def foto():
            return {**{x: Z["st"][x].copy() for x in Z["chiavi"]}, "campo_A": C.campo.A.copy(), "campo_E": C.campo.E.copy()}

        # ### la ripresa
        rimetti()
        pen = None
        for k in range(K_DA + 1, K_A + 1):
            if k == K_A:
                pen = foto()
            CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
        fin = foto()
        # ### i controlli della forma, DOPO la ripresa: il percorso di csv/ (la scena) contro quello del nucleo, e S3 col nucleo
        print("  la scena: MV.pezzi e' %s.%s (il nucleo: %s)" % (MV.pezzi.__module__, MV.pezzi.__qualname__, MV.pezzi is P_nucleo))
        rimetti()
        CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
        uno_csv = foto()
        rimetti()
        with col_nucleo(MV, P_nucleo):
            CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
        uno = foto()
        rimetti()
        with col_nucleo(MV, P_nucleo), MV.forma_esplicita("S3"):
            CS.tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
        uno_s3 = foto()
        esito("UN tick col percorso di csv/ (S1, la scena) = UN tick col percorso del nucleo (S1), AL BIT", all(np.array_equal(uno_csv[x], uno[x]) for x in uno),
              "le chiavi diverse %s" % [x for x in uno if not np.array_equal(uno_csv[x], uno[x])])
        diverse = [x for x in uno if not np.array_equal(uno[x], uno_s3[x])]
        esito("### DEVE fallire l'uguaglianza: UN tick col nucleo a S3 contro UN tick col nucleo a S1", len(diverse) > 0, "le chiavi diverse %s" % diverse)
        esito("la forma e i pezzi tornano quelli di prima dopo i contesti", MV.ATTIVA == "S1" and MV.pezzi is not P_nucleo, "%s" % MV.ATTIVA)
        Z["metti"]()
    print("-" * 130)
    h = hashlib.sha1()
    tutte = True
    for x in sorted(fin):
        uguale = np.array_equal(fin[x], X1[x]) and fin[x].dtype == X1[x].dtype and fin[x].shape == X1[x].shape
        tutte = tutte and uguale
        dmax = float(np.max(np.abs(fin[x] - X1[x]))) if fin[x].shape == X1[x].shape else float("nan")
        h.update(np.ascontiguousarray(fin[x]).tobytes())
        print("  %-10s %-12s %s: %s (max |diff| %.3e)" % (x, str(fin[x].shape), fin[x].dtype, "AL BIT" if uguale else "### DIVERSO", dmax))
    print("  lo sha1 dello stato a k %d (le chiavi in ordine): %s" % (K_A, h.hexdigest()))
    esito("lo stato a k %d = stato_%06d.npz del disco, ogni chiave, AL BIT" % (K_A, K_A), tutte)
    esito("### DEVE fallire l'uguaglianza: lo stato a k %d contro il file a k %d" % (K_A - 1, K_A), not all(np.array_equal(pen[x], X1[x]) for x in pen))
    print("=" * 130)
    print("  %d DEVE su %d   %s" % (sum(ok), len(ok), "TUTTI PASSATI" if all(ok) else "### CI SONO BUCHI"))
    print("=" * 130)
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
