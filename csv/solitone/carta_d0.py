# -*- coding: utf-8 -*-
r"""**`D0'`, PRIMA DELLA CORSA: IL TICK VIVO COMMUTA CON `R180` x `sigma_z`?** *(Luca, le decisioni dopo `ae60cfb6`; il task history `doc/TASK_HISTORY/2026-11-03_D0_ruotata_e_TS.md`)*
    python csv/solitone/carta_d0.py > doc/referti_l2/d0_simmetria_vivo.txt
### **Se commuta, la previsione di Luca** *(`D0'` e' l'immagine ruotata di `TP1000`)* **e' vera per costruzione fino all'arrotondamento; se no, cade sulle leggi.**
### **I DEVE:** `D-R2` la rotazione di tutto lo stato due volte e' l'identita' *(al bit, ogni chiave)*; `D-V` il vuoto ruotato di `F0` e' `-F0`; `D-T` il tick VIVO *(`AC.tick`, nella rampa
dalla partenza, e dopo la rampa dallo stato di `TM1000` a `13333`)*: `|T^n(R x) - R T^n(x)|` relativo sotto `TOLL_UGUALE`, ogni chiave; `D-T-F` *(deve fallire)* lo stesso con `U = 1`.
### **Registrata:** `D-P`, il tick legge `psi` per nodo? *(un tick con `psi` per nodo azzerato, contro quello vero)*.
### **La rotazione** e' quella di `carta_impulso` *(il centro d'inversione piu' vicino al centro della densita' di partenza; le chiavi per estremita' con `dove`, quelle per nodo con
`m -> m2 - m`; `U` su `psi_h` e `psi`)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

N_TICK = 10                    # ### il task history, sez. 2: 10 tick nella rampa e 10 dopo
T_STATO = 13333                # ### il primo stato completo di TM1000 (al bit di TP1000) oltre K
PER_ESTREMITA = ("psi_h", "phi_h")
CON_U = ("psi_h", "psi")       # ### le chiavi con le due componenti

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


def ruota(st, dove, nm, U):
    """### **`R` su tutto lo stato:** le chiavi per estremita' con `dove`, quelle per nodo con `nm`; `U` sulle chiavi a due componenti."""
    from solitone import carta_impulso as CI
    return {k: CI.applica(v, dove if k in PER_ESTREMITA else nm, U if k in CON_U else None) for k, v in st.items()}


def scarti(a, b):
    """### per chiave: `|a - b| / |b|` *(`|a - b|` se `|b| = 0`)*."""
    out = {}
    for k in b:
        nb = float(np.linalg.norm(b[k]))
        d = float(np.linalg.norm(a[k] - b[k]))
        out[k] = d / nb if nb > 0 else d
    return out


def main(argv):
    del argv
    import _deriva_congelato as DC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import carta_impulso as CI
    from solitone import corsa_accensione as CA
    for m in ("__init__", "accensione", "corsa_accensione", "carta_impulso"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    T_acc, _fine = CA.CORSE["TP1000"]
    K = int(round(T_acc / s))
    print("=" * 130)
    print("D0', PRIMA DELLA CORSA: IL TICK VIVO CONTRO R180 x sigma_z (Luca dopo ae60cfb6): %s (sol %s, s %g, eps %g); K %d; N_TICK %d; T_STATO %d; TOLL_UGUALE %g"
          % (CA.NOME, sol, s, V.EPS, K, N_TICK, T_STATO, CI.TOLL_UGUALE))
    print("=" * 130)
    testa = V.LP.leggi(os.path.join(CA.dir_json("TP1000"), CA.nomi("TP1000")[0]))
    f_st = os.path.join(CA.base_e("TM1000"), "stati", "TM1000", "TM1000_stato_%06d.npz" % T_STATO)
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        inc, L = z["inc"], z["L"]
        chiavi = [k for k, v in z["st"].items() if isinstance(v, np.ndarray)]
        salvato = {k: z["st"][k].copy() for k in chiavi}

        def metti(st):
            for k in chiavi:
                z["st"][k][...] = st[k]

        def foto():
            return {k: z["st"][k].copy() for k in chiavi}

        p0, info = V.partenza(sol, z, phi0, pK, s)
        metti(salvato)
        esito("DEVE PASSARE: P0 lo stato di partenza e' quello di TP1000 (mu al bit di quello del primo pezzo)", info["mu"] == testa["info"]["mu"], "mu %.15f" % info["mu"])
        ok_a, dd = CI.assi(inc, L)
        esito("DEVE PASSARE: P0-C l'arco k e' del nodo k // 3 (2k sul nodo, 2k+1 sul vicino lungo un asse fisso per k % 3)", ok_a, "gli assi %s" % dd)
        c0, _rho0 = CI.centro(z, p0)
        m2 = (int(round(2 * c0[0])), int(round(2 * c0[1])))
        v_ = np.arange(inc.n)
        dove = CI.rotazione(inc, L, dd, m2)
        nm = CI.nodo_di(L, m2[0] - v_ // L, m2[1] - v_ % L)
        print("  le chiavi dello stato %s; la rotazione attorno a (%.1f, %.1f)" % ({k: salvato[k].shape for k in chiavi}, 0.5 * m2[0], 0.5 * m2[1]))
        x0 = dict(salvato)
        x0["psi_h"] = p0.copy()
        sz = CI.SIGMA["sz"]
        rr = ruota(ruota(x0, dove, nm, sz), dove, nm, sz)
        esito("DEVE PASSARE: D-R2 la rotazione di tutto lo stato due volte e' l'identita' (al bit, ogni chiave)", all(np.array_equal(rr[k], x0[k]) for k in chiavi), "")
        rphi = CI.applica(phi0, dove)
        sv = float(np.linalg.norm(rphi + phi0) / np.linalg.norm(phi0))
        esito("DEVE PASSARE: D-V il vuoto ruotato di F0 e' -F0 (entro %g)" % CI.TOLL_UGUALE, sv <= CI.TOLL_UGUALE, "|R F0 + F0| / |F0| = %.3e" % sv)
        with np.load(f_st) as d:
            assert int(d["t"]) == T_STATO, "lo stato di TM1000 NON e' a %d" % T_STATO
            x1 = {k: d[k].copy() for k in chiavi}
        print("  lo stato dopo la rampa: %s (t %d, %d > K)" % (f_st, T_STATO, T_STATO))

        def corri(x, t0):
            metti(x)
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for t in range(t0 + 1, t0 + N_TICK + 1):
                    AC.tick(z, t, K)
            return foto()

        res = {}
        for lab, x, t0 in (("nella rampa (t 1 .. %d, lam fino a %.4f)" % (N_TICK, AC.lam_di(N_TICK, K)), x0, 0),
                           ("dopo la rampa (t %d .. %d, il tick intero)" % (T_STATO + 1, T_STATO + N_TICK), x1, T_STATO)):
            a = corri(x, t0)
            for nu in ("sz", "1"):
                U = CI.SIGMA[nu]
                b = corri(ruota(x, dove, nm, U), t0)
                sc = scarti(b, ruota(a, dove, nm, U))
                res[(lab, nu)] = sc
                print("    %-48s U %-2s: |T^%d(R x) - R T^%d(x)| relativo per chiave %s; il massimo %.4e"
                      % (lab, nu, N_TICK, N_TICK, {k: "%.3e" % v for k, v in sc.items()}, max(sc.values())))
        for lab in sorted({l for l, _n in res}):
            esito("DEVE PASSARE: D-T il tick VIVO commuta con R180 x sigma_z %s (entro %g, ogni chiave)" % (lab, CI.TOLL_UGUALE),
                  max(res[(lab, "sz")].values()) <= CI.TOLL_UGUALE, "il massimo %.3e" % max(res[(lab, "sz")].values()))
        lab0 = sorted({l for l, _n in res})[0]
        esito("DEVE FALLIRE: D-T-F lo stesso con U = 1 %s commuta (entro %g)" % (lab0, CI.TOLL_UGUALE),
              max(res[(lab0, "1")].values()) > CI.TOLL_UGUALE, "il massimo %.3e" % max(res[(lab0, "1")].values()))
        # ------------------------------------------------------------ D-P: il tick legge psi per nodo?
        a = corri(x0, 0)
        xz = dict(x0)
        xz["psi"] = np.zeros_like(x0["psi"])
        b = corri(xz, 0)
        uguali = all(np.array_equal(a[k], b[k]) for k in chiavi if k != "psi")
        print("  ### D-P (registrata): %d tick dalla partenza con psi per nodo AZZERATO contro quello vero: le altre chiavi uguali AL BIT? %s; psi per nodo dopo i tick: uguale? %s"
              % (N_TICK, uguali, np.array_equal(a["psi"], b["psi"])))
        metti(salvato)
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
