# -*- coding: utf-8 -*-
r"""**[M0908-L] LA LETTURA DEL SEGNO DELLA FORMA (a)** *(il mandato di Luca [M0908] `2026-11-22` `09:08`; la carta `doc/TASK_HISTORY/2026-11-22_caduta_libera.md`, sez. `1`; SOLA LETTURA, nessuna corsa lunga)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/caduta_segno.py > doc/referti_l2/caduta_segno.txt

**(0)** le righe del codice e delle carte, stampate dai sorgenti; **(a)** il vuoto della scena di `chi`, UN tick del tick U: `e^{-i omega} = <phi_0, phi_1>/|.|`; **(b)** l'onda piana: la risposta lineare di UN tick *(il metodo di T-L4b, le sue costanti `A_IMP`, `DK`, `H_CS`)*, la coppia piu' alta a `Gamma` con `E = -angle`, `d2 E/dk2` lungo `B_0`, la C-linearita'; **(c)** le varianti a `N` uniforme `1 - H_CS` *(V2 `cs = s N`; V3 la sola fase; V1 tutte e due; V4 `cs = s N` e la fase col segno opposto)*: `dE_top/dN`.
**`tick_var`** *(usato anche dalla caduta libera, [M0908-K])*: le righe di `chi_tick_v2.tick_chi_v2` SENZA l'evoluzione di `chi`, con `N` DATO per nodo, e due interruttori: `cs` *(`s N` o `s`)* e il segno della fase (a) *(`+1`, `-1`, `0` spenta)*.
"""
import inspect
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import chi_tick as CT  # noqa: E402
import chi_tick_v2 as CV2  # noqa: E402

VARIANTI = (("V2", True, 0), ("V3", False, +1), ("V1", True, +1), ("V4", True, -1))      # ### (nome, cs = s N, il segno della fase (a))


def tick_var(z, campo, s, e0, N, cs_N, segno):
    """### UN tick: `campo.spinta(1/2)`; `cs = s N` (o `s`); la fase (a) mezza `e^{+i segno e0 (N - 1)/2}`; il palindromo avvolto; la fase (a) mezza; `campo.spinta(1/2)`.
    ### Con `N = 1`, `cs_N` qualunque, `segno` qualunque: il tick U con `cs = s` AL BIT *(`s * 1.0 = s`, `exp(0) = 1`)*."""
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    mot, st, par = z["mot"], z["st"], z["par"]
    campo.spinta(0.5)
    mot.cs = float(s) * N if cs_N else np.full(mot.inc.n, float(s))
    mot.lambda_c = None
    if segno:
        CT.fase_a(mot, st, float(segno) * float(e0), N)
    with UO.avvolto(mot, campo, True):
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    if segno:
        CT.fase_a(mot, st, float(segno) * float(e0), N)
    campo.spinta(0.5)


def righe_di(f, pat, quante=3, larghezza=420):
    out = []
    with open(os.path.join(_RADICE, f), encoding="utf-8") as h:
        for i, r in enumerate(h, 1):
            if re.search(pat, r):
                out.append("    %s:%d  %s" % (f, i, r.strip()[:larghezza]))
                if len(out) >= quante:
                    break
    assert out, "### il testo %r NON e' in %s: FERMO" % (pat, f)
    return out


def main():
    import _presidio
    import s5_caduta_segno as T4B
    import gravita_due_corpi as GD
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "triangolo_chi_v4.py"))
    _presidio.avvia(os.path.join(_QUI, "gravita_due_corpi.py"))
    _presidio.avvia(__file__)
    A_IMP, DK, H_CS = T4B.A_IMP, T4B.DK, T4B.H_CS
    print("=" * 130)
    print("[M0908-L] LA LETTURA DEL SEGNO DELLA FORMA (a) (la carta sez. 1); le costanti di T-L4b: A_IMP %g, DK %g, H_CS %g" % (A_IMP, DK, H_CS))
    print("=" * 130)
    print("(0) LE RIGHE DEL CODICE (dai sorgenti di OGGI)")
    for r in inspect.getsource(CT.fase_a).rstrip().splitlines():
        print("    chi_tick.fase_a | " + r)
    for f, pat in (("doc/referti_l2/chi_tick.py", r"Fa = "), ("doc/referti_l2/chi_tick_v2.py", r"Fa = "), ("doc/referti_l2/chi_tick_v2.py", r"CT\.fase_a\(mot, st, P\.e0, N\)"),
                   ("csv/solitone/s5_caduta_segno.py", r"E = -np\.angle\(lam\)"), ("csv/solitone/s5_caduta_segno.py", r"mezza = np\.exp\(1j \* e0"),
                   ("csv/solitone/p6_bracci.py", r"TL\.fase_a\(mot, st, legge, e0, False\)"), ("csv/solitone/s5_coppia_lapse.py", r"def eps_top_tl4b")):
        for r in righe_di(f, pat, 2, 200):
            print(r)
    print("(0) LE RIGHE DELLE CARTE (dove la forma (a) e il suo segno furono decisi)")
    for f, pat in (("doc/TASK_HISTORY/2026-11-09_laterale_mb.md", r"LA FORMA \(a\)\*\* \*\(del guardiano\)"), ("doc/TASK_HISTORY/2026-11-09_laterale_mb.md", r"E_N = somma_k N_k h_k - eps_top"),
                   ("doc/TASK_HISTORY/2026-11-09_laterale_mb.md", r"\(iv\)\*\* \*\*il peso della materia"), ("doc/TASK_HISTORY/2026-11-21_lapse_u.md", r"D-CHI-FORMA-A = \(fa1\)"),
                   ("doc/referti_l2/s5_caduta_segno.txt", r"d2 eps/dk2"), ("doc/referti_l2/s5_caduta_segno.txt", r"LA LETTURA"), ("doc/referti_l2/s5_caduta_solitone.txt", r"LA LETTURA")):
        for r in righe_di(f, pat, 1):
            print(r)
    MT, _MTR, _T1, _TRU, _TV, PO = TC.moduli()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    with TC.scena() as Z:
        mot, st = Z["mot"], Z["st"]
        n, L, s = mot.inc.n, Z["L"], float(Z["s"])
        nodo = np.asarray(mot.inc.nodo)
        assert np.array_equal(nodo, np.repeat(np.arange(n), 6)), "i semiarchi non sono 6 per nodo in ordine: il reshape (n, 12) non vale"
        Z["g_e"] = np.zeros_like(Z["g_e"])
        MT.vuoto_fresco(Z, t0)
        C = PO.campi(Z, rho_c, e)
        base = {x: st[x].copy() for x in Z["chiavi"]}
        A0, E0, U0 = C.campo.A.copy(), C.campo.E.copy(), mot.geo.U.copy()
        print("-" * 130)
        print("### la scena: S162 (n %d, L %d), il vuoto fresco a t0 %r, g_e = 0, porto.campi; s %r; e0 %r (eps_top di T-L4b); max|psi| del vuoto %.3e" % (n, L, t0, s, e0, float(np.max(np.abs(st["psi_h"])))))

        def rimetti(psi=None):
            for x in Z["chiavi"]:
                st[x][...] = base[x]
            if psi is not None:
                st["psi_h"][...] = psi.reshape(st["psi_h"].shape)
            C.campo.A[...], C.campo.E[...] = A0, E0
            mot.geo.U[...] = U0
            mot.lambda_c = None

        # ### (a) il vuoto, UN tick
        rimetti()
        phi0 = st["phi_h"].copy()
        tick_var(Z["z"], C.campo, s, e0, np.ones(n), False, 0)
        zz = np.vdot(phi0, st["phi_h"])
        om = -float(np.angle(zz / abs(zz)))
        per = np.angle(st["phi_h"] / np.where(phi0 == 0, 1, phi0))[np.abs(phi0) > 0]
        print("(a) IL VUOTO, UN tick del tick U (cs = s): e^{-i omega} con omega = %+.10f (oppure %+.10f = omega - 2 pi: UN tick non decide); |<phi0,phi1>|/|phi0|^2 %.12f; la fase per componente da %+.6f a %+.6f" % (
            om, om - 2.0 * math.pi, abs(zz) / float(np.vdot(phi0, phi0).real), float(per.min()), float(per.max())))

        # ### (b) l'onda piana: la risposta lineare di UN tick
        A1, A2 = TO.vettori()
        B = 2.0 * np.pi * np.linalg.inv(np.array([A1, A2])).T
        bh = B[0] / np.linalg.norm(B[0])
        d0 = TO.scarti(Z["m1"], Z["m2"], 0.0, 0.0, L)[:, :2]

        def risposta(N, cs_N, segno, imm=False):
            R = np.zeros((n, 12, 12), dtype=complex)
            for j in range(12):
                us = []
                for f in (1.0, -1.0):
                    p = np.zeros((n, 12), dtype=complex)
                    p[0, j] = f * A_IMP * (1j if imm else 1.0)
                    rimetti(p)
                    tick_var(Z["z"], C.campo, s, e0, N, cs_N, segno)
                    us.append(st["psi_h"].reshape(n, 12).copy())
                R[:, :, j] = (us[0] - us[1]) / (2 * A_IMP)
                if imm and j == 0:
                    return R[:, :, 0]
            return R

        def A_di(R, kv):
            return np.einsum("x,xij->ij", np.exp(-1j * (d0 @ kv)), R)

        uno = np.ones(n)
        R0 = risposta(uno, False, 0)
        R0i = risposta(uno, False, 0, imm=True)
        clin = float(np.max(np.abs(R0i - 1j * R0[:, :, 0])) / np.max(np.abs(R0[:, :, 0])))
        G = A_di(R0, np.zeros(2))
        lam, Vv = np.linalg.eig(G)
        E = -np.angle(lam)
        o = np.argsort(E)
        top = [int(o[-2]), int(o[-1])]
        Qm = np.linalg.qr(Vv[:, top])[0]
        q = Qm[:, 0] / np.linalg.norm(Qm[:, 0])
        print("(b) L'ONDA PIANA, la risposta lineare di UN tick (cs = s, N = 1): la C-linearita' (la risposta a i e_0 contro i R e_0) %.3e%s" % (clin, "" if clin <= 1e-6 else "  ### SOPRA 1e-6: FERMO"))
        print("    i 12 autovalori a Gamma, E = -angle (ordinati): %s; |lambda| da %.12f a %.12f" % (" ".join("%+.7f" % E[i] for i in o), float(np.abs(lam).min()), float(np.abs(lam).max())))

        def sulla_cima(A):
            w, vr = np.linalg.eig(A)
            vr = vr / np.linalg.norm(vr, axis=0)
            ov = np.abs(vr.conj().T @ q) ** 2
            b = int(np.argmax(ov))
            return float(-np.angle(w[b])), float(ov[b])
        e_0, ov0 = sulla_cima(G)
        e_p, ovp = sulla_cima(A_di(R0, DK * bh))
        e_m, ovm = sulla_cima(A_di(R0, -DK * bh))
        d2 = (e_p - 2.0 * e_0 + e_m) / DK ** 2
        print("    LA COPPIA PIU' ALTA a Gamma: E %.10f e %.10f; contro e0 %.10f: lo scarto relativo %+.3e%s" % (E[top[0]], E[top[1]], e0, (E[top[1]] - e0) / e0, "" if abs(E[top[1]] - e0) <= 0.05 * e0 else "  ### OLTRE IL 5%: FERMO"))
        print("    la banda di q: E(0) %.10f, E(+dk) %.10f, E(-dk) %.10f (le sovrapposizioni %.4f %.4f %.4f); d2 E/dk2 lungo B_0 %+.6e: %s" % (
            e_0, e_p, e_m, ov0, ovp, ovm, d2, "la CIMA (la massa efficace NEGATIVA)" if d2 < 0 else "il FONDO (la massa efficace positiva)"))

        # ### (c) le varianti a N uniforme 1 - H_CS
        Nu = np.full(n, 1.0 - H_CS)
        print("(c) LE VARIANTI a N uniforme 1 - H_CS = %.6f: dE_top/dN = (E(N) - E(1)) / (N - 1); con d2 E/dk2 %s 0 il pacchetto va verso E_top piu' %s" % (
            1.0 - H_CS, "<" if d2 < 0 else ">", "ALTO" if d2 < 0 else "BASSO"))
        for nome, cs_N, segno in VARIANTI:
            Rv = risposta(Nu, cs_N, segno)
            ev, ovv = sulla_cima(A_di(Rv, np.zeros(2)))
            dEdN = (ev - e_0) / (-H_CS)
            verso = "VERSO N piu' BASSO" if (dEdN < 0) == (d2 < 0) else "VIA (verso N piu' ALTO)"
            print("    %s (cs %s, la fase (a) %s): E_top(N) %.10f (la sovrapposizione %.4f); dE_top/dN %+.6e; contro le parti: s dE/dcs = %s, -segno e0 = %+.6f; il pacchetto: %s" % (
                nome, "s N" if cs_N else "s  ", {0: "spenta", 1: "+", -1: "-"}[segno], ev, ovv, dEdN, "(V2)" if nome == "V2" else "-", -float(segno) * e0, verso))
        rimetti()
        Z["metti"]()
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
