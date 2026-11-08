# -*- coding: utf-8 -*-
r"""**v2, IL BRACCIO `0` DELLO ZERO SIMMETRICO NEL NUCLEO** *(Luca `2026-11-08` `14:19`; il task history `doc/TASK_HISTORY/2026-11-08_zero_simmetrico_nel_nucleo.md`, sez. `3`)*. [[PIANO-2D-3D]]

    python csv/solitone/zero_nel_nucleo.py --radice <albero> --uscita <file.json> [--doppio]
    python csv/solitone/zero_nel_nucleo.py --confronta <padre.json> <nuovo.json> <doppio.json> > doc/referti_l2/zero_nel_nucleo.txt

### **Il tick della corsa** *(`accensione.tick`, dentro `SF.forma(VC.FORMA)` e `BE.conv(DC.ZERO)`, come la corsa)* **sull'albero `--radice`** *(i suoi `csv/` e `primo_ordine/` per
primi in `sys.path`: il nucleo VECCHIO col suo avvolgimento, o il NUOVO senza)*: **(D) `N_D` tick dallo stato di `TBS` al tick `100000`** *(dopo la rampa)*; **(R) `N_R` tick
dalla partenza della scena** *(nella rampa: `tick_acceso`, un altro percorso)*. **Gli `sha` di ogni chiave.** **`--doppio`:** **l'avvolgimento di prima rimesso SOPRA il nucleo
nuovo** *(lo zero due volte: DEVE FALLIRE)*. **`--confronta`:** **`Z0` padre = nuovo AL BIT, ogni chiave, (D) e (R); `Z0-F` doppio != padre.**
"""
import json
import os
import sys

TICK0 = 100000
N_D = 100
N_R = 50
FILE_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_%06d_completo.npz" % TICK0)


def prendi(argv, nome):
    return argv[argv.index(nome) + 1] if nome in argv else None


def doppio_avvolgimento():
    """### **L'avvolgimento di prima** *(`convenzione_simmetrica` composta con `convenzione_alternativa`)* **sopra le funzioni del nucleo nuovo**: lo zero DUE volte."""
    import contextlib
    import numpy as np
    import flussi_parziali as FP

    @contextlib.contextmanager
    def cm():
        g0, hp0, hf0 = FP.grover, FP.hop_psi, FP.hop_phi

        def alt_g(mot, vista, f):
            out = g0(mot, vista, f)
            vista *= np.conj(FP.z_nodo(mot, f)[mot.inc.nodo])
            return out

        def alt_h(f0):
            def h(mot, x, f):
                out = f0(mot, x, f)
                zz = np.repeat(np.conj(FP.z_arco(mot, f)), 2, axis=0)
                x *= zz if x.ndim == 2 else zz[:, 0]
                return out
            return h

        def comp(oggi, alt):
            def f(mot, x, fr):
                oggi(mot, x, 0.5 * fr)
                return alt(mot, x, 0.5 * fr)
            return f
        FP.grover, FP.hop_psi, FP.hop_phi = comp(g0, alt_g), comp(hp0, alt_h(hp0)), comp(hf0, alt_h(hf0))
        try:
            yield
        finally:
            FP.grover, FP.hop_psi, FP.hop_phi = g0, hp0, hf0
    return cm()


def corri(radice, uscita, doppio):
    for p in (os.path.join(radice, "primo_ordine", "leggi"), os.path.join(radice, "primo_ordine"), os.path.join(radice, "csv")):
        sys.path.insert(0, p)
    import contextlib
    import numpy as np
    import _deriva_congelato as DC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import _dove_va_la_materia as DV
    import flussi_parziali as FP
    from solitone import accensione as AC
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    assert os.path.normcase(os.path.dirname(os.path.abspath(FP.__file__))) == os.path.normcase(os.path.join(os.path.abspath(radice), "primo_ordine")), ("il nucleo NON e' quello dell'albero", FP.__file__)
    for m in (FP.__file__, AC.__file__, BE.__file__):
        _presidio.avvia(m)
    sol, vuoto, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TBS"][0] / s))
    out = {"radice": radice, "doppio": doppio, "flussi_parziali": FP.__file__, "K": K}
    extra = doppio_avvolgimento() if doppio else contextlib.nullcontext()
    with V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        partenza = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        for k, v in salvato.items():
            z["st"][k][...] = v
        chiavi = sorted(k for k, v in z["st"].items() if isinstance(v, np.ndarray))
        # ---------------------------------------------- (R) nella rampa, dalla partenza
        for k in chiavi:
            z["st"][k][...] = partenza[k]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO), extra:
            for t in range(1, N_R + 1):
                AC.tick(z, t, K)
        out["R"] = V.shas(z)
        # ---------------------------------------------- (D) dopo la rampa, dallo stato di TBS
        with np.load(FILE_LIB) as d:
            assert int(d["t"]) == TICK0
            for k in chiavi:
                z["st"][k][...] = d[k]
        extra = doppio_avvolgimento() if doppio else contextlib.nullcontext()
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO), extra:
            for t in range(TICK0 + 1, TICK0 + N_D + 1):
                AC.tick(z, t, K)
        out["D"] = V.shas(z)
    with open(uscita, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("scritto %s: R %d chiavi, D %d chiavi" % (uscita, len(out["R"]), len(out["D"])))


def confronta(fp, fn, fd):
    _QUI = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(_QUI))
    import _presidio
    _presidio.avvia(__file__)
    P_, N_, D_ = (json.load(open(f, encoding="utf-8")) for f in (fp, fn, fd))
    ok = [0, 0]
    falliti = []

    def esito(che, passa, nota):
        ok[1] += 1
        ok[0] += int(passa)
        if not passa:
            falliti.append(che)
        print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 130)
    print("v2, IL BRACCIO 0 DELLO ZERO SIMMETRICO NEL NUCLEO: il padre %s (%s), il nuovo %s (%s), il doppio %s; N_D %d dal tick %d di TBS, N_R %d nella rampa"
          % (fp, P_["radice"], fn, N_["radice"], fd, N_D, TICK0, N_R))
    print("=" * 130)
    for seg, che in (("D", "dopo la rampa, %d tick dallo stato di TBS" % N_D), ("R", "nella rampa (tick_acceso), %d tick dalla partenza" % N_R)):
        div = sorted(k for k in P_[seg] if P_[seg][k] != N_[seg].get(k))
        esito("DEVE PASSARE: Z0-%s il nucleo NUOVO senza avvolgimento = il VECCHIO con l'avvolgimento, AL BIT, ogni chiave: %s" % (seg, che), not div and set(P_[seg]) == set(N_[seg]),
              "%d chiavi; diverse %s" % (len(P_[seg]), div))
        divd = sorted(k for k in P_[seg] if P_[seg][k] != D_[seg].get(k))
        esito("DEVE FALLIRE: Z0-F-%s il nucleo nuovo CON l'avvolgimento di prima (lo zero due volte) = il vecchio: %s" % (seg, che), bool(divd), "diverse %s" % divd)
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (ok[0], ok[1], len(falliti), falliti))
    return 0 if not falliti else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--confronta" in a:
        i = a.index("--confronta")
        sys.exit(confronta(a[i + 1], a[i + 2], a[i + 3]))
    corri(prendi(a, "--radice"), prendi(a, "--uscita"), "--doppio" in a)
