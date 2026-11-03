# -*- coding: utf-8 -*-
r"""**`TS`, PRIMA DEL CODICE: LA PARTENZA PUO' ESSERE SIMMETRICA SENZA SCEGLIERE?** *(Luca, le decisioni dopo `ae60cfb6`, (b); il task history `doc/TASK_HISTORY/2026-11-03_D0_ruotata_e_TS.md`)*
    python csv/solitone/carta_ts.py > doc/referti_l2/ts_condizione.txt
### **La condizione** *(il task history, sez. 1)*: con l'inviluppo sul NODO simmetrico *(`inv(R v) = inv(v)`)* il ruotato vale `R psi = c psi` **se e solo se** `P q = c q`, con
`(P q)[a, s] = sigma_z q[a, 1 - s]` *(l'asse `a`, l'estremita' `s` della cella: `0` sul nodo, `1` sul vicino; `q` di `12` componenti nell'ordine di `reshape(n, 12)`)*.
### **Il tick commuta con `R180` x `sigma_z`** *(`carta_d0`)*, quindi `G = A(Gamma)` commuta con `P` e **la coppia di `B` a `Gamma` e' invariante:** o `P = +-1` su tutta la coppia *(ogni
`q` va bene: nessuna scelta)*, o la coppia ha un `+1` e un `-1` *(la `q` simmetrica e' una SCELTA DI SETTORE: di Luca)*. **Si misura.**
### **I DEVE:** `TS-G` `G` commuta con `P` *(`sigma_z`)*; `TS-G-F` *(deve fallire)* con `U = 1`; `TS-Q` la coppia e' invariante sotto `P` *(`|P Q - Q M|`)*; **sul vuoto `F0` e su `F3`** *(Luca dopo `eaa5e3ec`: `F3` il vuoto predefinito; una matrice `12 x 12` in piu', costo trascurabile)*. **Registrati:** gli autovalori di `M`, la
`q` di oggi contro `P`, la simmetria dell'inviluppo sul nodo *(la densita' di `pK` per nodo contro la sua ruotata)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

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


def matrice_P(U):
    """### **`P` sulla cella** *(12 x 12)*: `(P q)[a, s] = U q[a, 1 - s]`, l'indice `4 a + 2 s + componente` *(`reshape(n, 12)`: le estremita' `2k`, `2k + 1` degli archi `k = 3 v + a`)*."""
    P = np.zeros((12, 12), dtype=complex)
    for a in range(3):
        for s in range(2):
            P[4 * a + 2 * s:4 * a + 2 * s + 2, 4 * a + 2 * (1 - s):4 * a + 2 * (1 - s) + 2] = U
    return P


def main(argv):
    del argv
    import _presidio
    import _vuoto_vivo_B as V
    import _solitone_dal_fondo as SD
    import _energia_del_legame as EL
    from solitone import carta_impulso as CI
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "carta_impulso", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    CB = V.CB                  # ### la coppia come V.partenza (il modulo che usa la corsa)
    sol, vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("TS, PRIMA DEL CODICE (Luca dopo ae60cfb6, (b)): %s (sol %s, s %g, eps %g); TOLL_UGUALE %g" % (CA.NOME, sol, s, V.EPS, CI.TOLL_UGUALE))
    print("=" * 130)
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        inc, L = z["inc"], z["L"]
        gr = V.LP.leggi(os.path.join(CB.DIR_JSON, "griglia.json"))[V.CO.NOME_EPS]
        th, fi = gr["minimo"]["theta"], gr["minimo"]["phi"]
        vuoti = {"F0": phi0, "F3": SD.fondo_con_fasi(inc, L, tuple(dict(SD.FASI)["F3"]))}   # ### Luca dopo eaa5e3ec: TS anche su F3 (il vuoto predefinito)
        for nv, phv in vuoti.items():
            print("-" * 130)
            print("### IL VUOTO %s" % nv)
            q1, q2, E0, G = CB.coppia(z, phv)
            q = math.cos(th) * q1 + np.exp(1j * fi) * math.sin(th) * q2
            lam = np.linalg.eigvals(G)
            E = np.sort(-np.angle(lam) / CB.S)
            print("  la coppia di B a Gamma (CB.coppia, come V.partenza): E0 %.12f; i tre livelli in alto %s; la degenerazione E[-1] - E[-2] = %.3e; theta %.6f phi %.6f"
                  % (E0, ["%.12f" % e for e in E[-3:]], E[-1] - E[-2], th, fi))
            cm = {}
            for nu in ("sz", "1", "sx", "sy"):
                P = matrice_P(CI.SIGMA[nu])
                cm[nu] = float(np.linalg.norm(G @ P - P @ G) / np.linalg.norm(G))
            print("  |G P - P G| / |G| per U: %s" % {k: "%.3e" % v for k, v in cm.items()})
            esito("DEVE PASSARE: TS-G (%s) G" % nv + " = A(Gamma) commuta con P (U = sigma_z) entro %g" % CI.TOLL_UGUALE, cm["sz"] <= CI.TOLL_UGUALE, "%.3e" % cm["sz"])
            esito("DEVE FALLIRE: TS-G-F (%s) G" % nv + " commuta con P per U = 1 entro %g" % CI.TOLL_UGUALE, cm["1"] > CI.TOLL_UGUALE, "%.3e" % cm["1"])
            P = matrice_P(CI.SIGMA["sz"])
            Q = np.stack([q1, q2], axis=1)
            M = Q.conj().T @ P @ Q
            rq = float(np.linalg.norm(P @ Q - Q @ M))
            esito("DEVE PASSARE: TS-Q (%s) la" % nv + " coppia e' invariante sotto P (|P Q - Q M| entro %g)" % CI.TOLL_UGUALE, rq <= CI.TOLL_UGUALE, "%.3e" % rq)
            mu_, W = np.linalg.eig(M)
            print("  ### M = Q^+ P Q (la P sulla coppia): %s; gli autovalori %s" % (np.array2string(M, precision=6), ["%+.6f %+.6fi" % (x.real, x.imag) for x in mu_]))
            for j in range(2):
                qq = Q @ W[:, j]
                qq = qq / np.linalg.norm(qq)
                Eq = -np.angle(complex(np.vdot(qq, G @ qq))) / CB.S
                bl = float(np.linalg.norm(G @ qq - complex(np.vdot(qq, G @ qq)) * qq))
                c1, c2 = complex(np.vdot(q1, qq)), complex(np.vdot(q2, qq))
                th_j = math.atan2(abs(c2), abs(c1))
                fi_j = math.atan2((c2 * c1.conjugate()).imag, (c2 * c1.conjugate()).real)
                print("    l'autovettore di P nella coppia con autovalore %+.6f: E %.12f; |G q - <G> q| %.3e; nella base (q1, q2) theta %.6f phi %+.6f"
                      % (mu_[j].real, Eq, bl, th_j, fi_j))
            c = complex(np.vdot(q, P @ q) / np.vdot(q, q))
            print("  ### la q DI OGGI (theta %.6f phi %.6f, griglia.json): c = <q, P q> = %+.6f %+.6fi; |P q - c q| / |q| = %.4e"
                  % (th, fi, c.real, c.imag, float(np.linalg.norm(P @ q - c * q) / np.linalg.norm(q))))
        # ------------------------------------------------------------ l'inviluppo sul nodo: la densita' di pK per nodo, contro la sua ruotata
        st = dict(z["st"])
        st["psi_h"] = pK
        rK, _l = EL.densita(inc, st)
        v_ = np.arange(inc.n)
        cK1, cK2, _x, _y = TO.centro(rK, v_ // L, v_ % L, L)
        m2K = (int(round(2 * cK1)), int(round(2 * cK2)))
        for lab, m2 in (("attorno al centro d'inversione piu' vicino al centro di pK", m2K), ("attorno a (40.5, 40.5), quello di D0R", (81, 81))):
            nm = CI.nodo_di(L, m2[0] - v_ // L, m2[1] - v_ % L)
            print("  ### l'inviluppo sul NODO (la densita' di pK per nodo) %s (%.1f, %.1f): |rho_K(R v) - rho_K(v)| / |rho_K| = %.4e"
                  % (lab, 0.5 * m2[0], 0.5 * m2[1], float(np.linalg.norm(rK[nm] - rK) / np.linalg.norm(rK))))
        print("  il centro di pK per nodo (indici) (%.6f, %.6f)" % (cK1, cK2))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
