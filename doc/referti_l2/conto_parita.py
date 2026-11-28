# -*- coding: utf-8 -*-
r"""**[M1205] H-2, IL CONTO DELLA PARITA' SUL VUOTO FRESCO** *(DECISIONE DI LUCA, 2026-11-28 12:05, punto 3; la carta `doc/CARTA_mitosi.md`,
«H-2, LA CARTA: LA COPPIA IN ANTIFASE E L'EREDITA' PER PARITA' -- IL CONTO ESPLICITO»; nessun tick, nessuna regola nel simulatore)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/conto_parita.py > doc/referti_l2/conto_parita.txt

Il vuoto fresco della scena *(`phi_v`, `+-1`)*, l'arco `39123` *(il centro)*; `s_a = sign(Re f[a,0] conj f[a,1])`; `delta = pi - |Phi|` di
`flusso_nascite.delta_di`. (P0) i due triangoli di partenza; (P1) il nodo solo per MEDIA *(`nasci_array`)*; (P2) il nodo solo per SEGNO
*(`A = +1`, `C = -A s_ij`, `D = -A s_ik`, `E = -A s_il`)*; (P3) la coppia per SEGNO *(`A = C = +1`, `B = A C s_ij`, `D, E, F, G` come nella carta)*;
(P3-neg) DEVE FALLIRE: `B = -s_ij`. Il segno del cammino `i -> j` prima e dopo.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import flusso_nascite as FN  # noqa: E402

CFM, MR, MR2, RV = FN.CFM, FN.MR, FN.MR2, FN.RV
ARCO = 39123
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-104s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "flusso_nascite.py"))
    _presidio.avvia(__file__)
    print("=" * 134)
    print("[M1205] H-2, IL CONTO DELLA PARITA' SUL VUOTO FRESCO (l'arco %d); nessun tick" % ARCO)
    print("=" * 134)
    with CFM.V6.GD.TC.scena() as Z:
        nodo0 = np.asarray(Z["mot"].inc.nodo)
        ii, jj, n0 = nodo0[0::2].astype(np.int64), nodo0[1::2].astype(np.int64), int(Z["mot"].inc.n)
        pv = np.asarray(Z["phi_v"]).copy()
        ori0 = RV.ori_toro(Z)
        Z["metti"]()
    m = len(ii)
    f = pv.reshape(m, 2)
    a = ARCO
    i, j, k, l = MR2.indici_nascita_v2(ii, jj, ori0, a)

    def s(x, y):
        q = MR.arco_fra(ii, jj, x, y)
        return int(np.sign(np.real(f[q, 0] * np.conj(f[q, 1]))))

    def val(x, verso):
        """### il valore dell'estremita' di `x` sull'arco verso `verso` (nel fresco)."""
        q = MR.arco_fra(ii, jj, x, verso)
        return f[q, 0] if ii[q] == x else f[q, 1]
    sij, sik, skj, sil, slj = s(i, j), s(i, k), s(k, j), s(i, l), s(l, j)
    print("  la stella: i %d, j %d, k %d, l %d; i segni s_ij %+d, s_ik %+d, s_kj %+d, s_il %+d, s_lj %+d" % (i, j, k, l, sij, sik, skj, sil, slj))
    d0 = FN.delta_di(ii, jj, pv, [tuple(sorted((i, j, k))), tuple(sorted((i, j, l)))])
    esito("(P0) i due triangoli di partenza a flusso pi (prodotti dei segni -1)", np.all(d0 == 0.0) and sik * skj * sij == -1 and sil * slj * sij == -1, "delta %s" % d0.tolist())
    # ### P1: il nodo solo per media
    ii2, jj2, ph2, _m = FN.nasci(ii, jj, pv, {"i": i, "j": j, "k": k, "l": l, "n": n0}, a, None)
    amp = np.min(np.abs(ph2.reshape(len(ii2), 2)[-4:]), axis=1)
    esito("(P1) il nodo solo per MEDIA: i buchi su n - k, n - l (|phi| < 1e-6), 1 su n - i, n - j", bool(amp[2] < 1e-6 and amp[3] < 1e-6 and amp[0] == 1 and amp[1] == 1), "|phi| %s" % ["%.2e" % v for v in amp])
    keep = np.ones(m, dtype=bool)
    keep[a] = False

    def costruisci(nuovi):
        """### `nuovi`: `[(p, q, f_p, f_q)]`, gli archi nuovi coi valori alle due estremita'."""
        I = np.concatenate([ii[keep], [x[0] for x in nuovi]])
        J = np.concatenate([jj[keep], [x[1] for x in nuovi]])
        ph = np.concatenate([pv[np.repeat(keep, 2)], np.array([v for x in nuovi for v in (x[2], x[3])], dtype=pv.dtype)])
        return I, J, ph
    # ### P2: il nodo solo per segno (l'estremita' del vicino: quella verso i per k e l, quella dell'arco tolto per i e j)
    n = n0
    A = +1
    C, D, E = -A * sij, -A * sik, -A * sil
    vi, vj, vk, vl = (f[a, 0] if ii[a] == i else f[a, 1]), (f[a, 1] if ii[a] == i else f[a, 0]), val(k, i), val(l, i)
    I, J, ph = costruisci([(n, i, A * vi, vi), (n, j, C * vj, vj), (n, k, D * vk, vk), (n, l, E * vl, vl)])
    T = FN.triangoli(FN.adiacenza(I, J), solo=[n])
    d2 = FN.delta_di(I, J, ph, T)
    esito("(P2) il nodo solo per SEGNO: i %d triangoli nuovi a flusso pi; il cammino i - n - j ha segno -s_ij (ROVESCIATO)" % len(T),
          len(T) == 4 and np.all(np.abs(d2) < 1e-12) and A * C == -sij, "delta %s; A C %+d contro s_ij %+d" % (["%.1e" % v for v in d2], A * C, sij))
    # ### P3: la coppia per segno; P3-neg con B rovesciato
    n1, n2 = n0, n0 + 1
    for nome, rov in (("(P3) la coppia per SEGNO (A = C = +1, B = s_ij)", False), ("(P3-neg) DEVE FALLIRE: la coppia con B = -s_ij", True)):
        A, C = +1, +1
        B = A * C * sij * (-1 if rov else 1)
        D, E, F, G = -A * sik, -A * sil, -C * skj, -C * slj
        vk_i, vl_i, vk_j, vl_j = val(k, i), val(l, i), val(k, j), val(l, j)
        I, J, ph = costruisci([(n1, i, A * vi, vi), (n1, n2, 1.0 + 0j, B * (1.0 + 0j)), (n2, j, C * vj, vj),
                               (n1, k, D * vk_i, vk_i), (n1, l, E * vl_i, vl_i), (n2, k, F * vk_j, vk_j), (n2, l, G * vl_j, vl_j)])
        T = FN.triangoli(FN.adiacenza(I, J), solo=[n1, n2])
        d3 = FN.delta_di(I, J, ph, T)
        amp3 = np.min(np.abs(ph.reshape(len(I), 2)[-7:]), axis=1)
        if not rov:
            esito(nome + ": i 6 triangoli a flusso pi, nessun arco nullo; il cammino i - n1 - n2 - j ha segno s_ij (CONSERVATO)",
                  len(T) == 6 and np.all(np.abs(d3) < 1e-12) and np.all(amp3 == 1.0) and A * B * C == sij,
                  "delta %s; A B C %+d contro s_ij %+d; i triangoli %s" % (["%.1e" % v for v in d3], A * B * C, sij, T))
        else:
            esito(nome + ": i triangoli (n1, n2, k) e (n1, n2, l) NON a flusso pi (delta = pi)", int(np.sum(np.abs(d3 - np.pi) < 1e-12)) == 2,
                  "delta %s" % ["%.2f" % v for v in d3])
    fall = [k_ for k_, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 134)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
