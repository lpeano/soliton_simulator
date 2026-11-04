# -*- coding: utf-8 -*-
r"""**`E_leg`: IL `RuntimeWarning` VISTO IN `B0`** *(Luca `2026-11-04` `09:00`; il task history `doc/TASK_HISTORY/2026-11-03_TB3_bordo_assorbente.md`, sezione 5)*
    python csv/solitone/carta_e_leg.py --diagnosi > doc/referti_l2/e_leg_diagnosi.txt
    python csv/solitone/carta_e_leg.py --prova    > doc/referti_l2/e_leg_prova.txt
### **`--diagnosi`** *(prima della correzione)*: ogni avviso numerico con la catena delle chiamate *(file, funzione)*, sui passi di `B0`: la scena, `protetto.e_K`, il libro dei conti sullo stato di
`B0` e sullo stato della corsa a `t 0`; per ogni chiamata di `_scomposizione_solitone.parti`, i nodi con `Lambda = 0` e la `rho` su di loro. ### **`--prova`** *(dopo)*: `E0` le cinque uscite di
`parti` e `e_K` AL BIT fra la versione di `PRIMA` *(dal blob di git)* e quella di oggi sugli stati di `TS` *(`30000`)*, `TF3` *(`16000`)*, `TF3C` *(`30000`)* *(i `.npz` di ripresa, verificati con lo
`sha_fine`)* e della corsa a `t 0`; `E1` `E_leg` finito con la versione di oggi sullo stato di `B0`, della corsa a `t 0`, uniforme di `e_K`; `E1-F` *(deve fallire)* la versione di `PRIMA` finita
sullo stato uniforme di `e_K`.
"""
import os
import subprocess
import sys
import traceback
import types
import warnings

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

PRIMA = "45e996a1"             # ### un commit prima della correzione (_scomposizione_solitone.py invariato da molto prima)
STATI = (("TS", "TS.npz"), ("TF3", "TF3.npz"), ("TF3C", "TF3C.npz"))

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def vecchio():
    """### **`_scomposizione_solitone` di `PRIMA`**, dai byte del blob *(non dal disco)*, come modulo a se'."""
    rad = os.path.dirname(os.path.dirname(_QUI))
    src = subprocess.check_output(["git", "show", "%s:csv/_scomposizione_solitone.py" % PRIMA], cwd=rad)
    m = types.ModuleType("_scomposizione_solitone_prima")
    m.__file__ = os.path.join(rad, "csv", "_scomposizione_solitone.py")
    exec(compile(src, "%s:csv/_scomposizione_solitone.py" % PRIMA, "exec"), m.__dict__)
    return m


def catena():
    """### **La catena delle chiamate** *(i file del repo, `file:funzione`)*, senza questa carta e senza `warnings`."""
    out = []
    for fr in traceback.extract_stack()[:-2]:
        f = fr.filename.replace("\\", "/")
        if "soliton_simulator" in f and "carta_e_leg" not in f:
            out.append("%s:%s" % (f.split("soliton_simulator/")[-1], fr.name))
    return " <- ".join(reversed(out))


def main(argv):
    modo = argv[0] if argv else ""
    assert modo in ("--diagnosi", "--prova"), "uso: --diagnosi | --prova"
    import _deriva_congelato as DC
    import _libro_dei_conti as LC
    import _presidio
    import _scomposizione_solitone as SC
    import _screening_forme_s3 as SF
    import _solitone_dal_fondo as SD
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    for m in ("__init__", "corsa_accensione", "protetto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_scomposizione_solitone.py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("E_leg (Luca 09:00): %s; %s (s %g, eps %g); PRIMA %s" % (modo, CA.NOME, s, V.EPS, PRIMA))
    print("=" * 130)
    avvisi = []
    parti_vere = SC.parti

    def parti_spia(inc, mot, st):
        lam = np.zeros(inc.n)
        np.add.at(lam, inc.nodo, np.abs(st["phi_h"]) ** 2)
        rho = np.zeros(inc.n)
        np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
        z0 = lam == 0.0
        print("    parti(): %d nodi; Lambda = 0 su %d; rho su quei nodi: min %.6e max %.6e; Lambda min %.6e; chiamata da %s"
              % (inc.n, int(z0.sum()), float(rho[z0].min()) if z0.any() else float("nan"), float(rho[z0].max()) if z0.any() else float("nan"), float(lam.min()), catena()))
        return parti_vere(inc, mot, st)

    def mostra(message, category, filename, lineno, file=None, line=None):
        avvisi.append("%s:%d %s: %s; chiamata da %s" % (os.path.basename(filename), lineno, category.__name__, message, catena()))
    with warnings.catch_warnings():
        warnings.simplefilter("always")
        warnings.showwarning = mostra
        if modo == "--diagnosi":
            SC.parti = parti_spia
        try:
            with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
                print("  ### (1) la scena V.scena: %d avvisi" % len(avvisi))
                chiavi = [k for k, v in z["st"].items() if isinstance(v, np.ndarray)]
                salvato = {k: z["st"][k].copy() for k in chiavi}
                p0, _info = V.partenza(sol, z, phi0, pK, s)
                for k in chiavi:
                    z["st"][k][...] = salvato[k]
                F3 = SD.fondo_con_fasi(z["inc"], z["L"], tuple(dict(SD.FASI)["F3"]))
                n0 = len(avvisi)
                e_K = P.e_K(z)
                print("  ### (2) protetto.e_K: e_K %.15e; %d avvisi" % (e_K, len(avvisi) - n0))

                def stato(psi):
                    st = {k: v.copy() for k, v in salvato.items()}
                    st["psi_h"][...] = psi
                    st["phi_h"][...] = F3
                    return st
                st_b0, st_t0 = stato(np.zeros_like(p0)), stato(p0)
                incu, motu, stu = SC.stato_uniforme(z["L"], z["Q"], z["m1"], z["m2"])
                with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                    for nome, st in (("lo stato di B0 (psi 0, phi F3)", st_b0), ("la corsa a t 0 (psi p0, phi F3)", st_t0)):
                        n0 = len(avvisi)
                        cc = LC.conti_per_nodo(z["inc"], z["mot"], st, e_K, V.LAM_ZERO, z["par"])
                        print("  ### (3) il libro dei conti su %s: leg finito %s, somma %.15e; %d avvisi" % (nome, bool(np.all(np.isfinite(cc["leg"]))), float(np.sum(cc["leg"])), len(avvisi) - n0))
                    if modo == "--prova":
                        SV = vecchio()
                        st_npz = []
                        for nome, f in STATI:
                            rr, _c, _d, _a = CA.serie(nome)
                            with np.load(os.path.join(CA.DIR_NPZ, f)) as d:
                                st = {k: d[k].copy() for k in d.files if k != "t"}
                                t = int(d["t"])
                            sh = {k: SFM.sha(v) for k, v in sorted(st.items())}
                            esito("DEVE PASSARE: lo stato %s (%s) e' lo sha_fine dell'ultimo pezzo (t1 %d)" % (nome, f, rr[-1]["t1"]), sh == rr[-1]["sha_fine"] and t == rr[-1]["t1"], "t %d" % t)
                            st_npz.append(("%s a t %d" % (nome, t), st))
                        uguali = []
                        for nome, st in st_npz + [("la corsa a t 0", st_t0), ("lo stato di B0", st_b0)]:
                            a, b = SV.parti(z["inc"], z["mot"], st), SC.parti(z["inc"], z["mot"], st)
                            uguali.append(all(np.array_equal(x, y) for x, y in zip(a, b)))
                            print("    E0 %s: PRIMA %s; OGGI %s" % (nome, ", ".join("%.17g" % x for x in a), ", ".join("%.17g" % x for x in b)))
                        ea, eb = SV.parti(incu, motu, stu), SC.parti(incu, motu, stu)
                        ek_ug = ea[0] / ea[3] == eb[0] / eb[3]
                        esito("DEVE PASSARE: E0 le cinque uscite di parti AL BIT, PRIMA e OGGI, su %d stati (TS, TF3, TF3C, t 0, B0), e e_K al bit" % len(uguali), all(uguali) and ek_ug,
                              "e_K PRIMA %.17g OGGI %.17g" % (ea[0] / ea[3], eb[0] / eb[3]))
                        fin = []
                        for nome, st in (("B0", st_b0), ("t 0", st_t0)):
                            fin.append(bool(np.isfinite(SC.parti(z["inc"], z["mot"], st)[2])))
                        fin.append(bool(np.isfinite(eb[2])))
                        esito("DEVE PASSARE: E1 E_leg finito OGGI sullo stato di B0, della corsa a t 0, uniforme di e_K", all(fin), "E_leg uniforme OGGI %.17g" % eb[2])
                        esito("DEVE FALLIRE: E1-F E_leg finito con PRIMA sullo stato uniforme di e_K", not bool(np.isfinite(ea[2])), "E_leg uniforme PRIMA %r" % ea[2])
                for k in chiavi:
                    z["st"][k][...] = salvato[k]
        finally:
            SC.parti = parti_vere
    print("-" * 130)
    print("### GLI AVVISI (%d), con la catena delle chiamate:" % len(avvisi))
    for a in avvisi:
        print("    " + a)
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s; avvisi %d" % (OK[0], OK[1], len(FALLITE), FALLITE, len(avvisi)))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
