# -*- coding: utf-8 -*-
r"""**[M1658-A] L'ABLAZIONE DELLO SPETTRO: UN PEZZO ALLA VOLTA** *(Luca, 2026-11-23; la carta `doc/CARTA_fondo_giusto.md`, sez. `4`; in memoria, nessuna corsa, il nucleo non si tocca)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/ablazione.py > doc/referti_l2/ablazione.txt

**Il metodo di `spettro_gap_v2.main`** *(la risposta lineare di UN tick sul vuoto fresco della scena di chi; `A(k)` sulla griglia `96 x 96`)* **col tick di `caduta_segno_v2.tick_var` riga per riga** *(`cs = s`, segno `0`)* **e la lista `salta` di `percorri_tick`.** **Le varianti:** **(0)** nessuna *(il caso noto: `spettro.npz` AL BIT)*; **(i)** `salta` `CAMM-MONETA-SPIN`; **(ii)** lo zero di prima *(le voci `grover`, `spostamento_trasporto`, `grover_scalare`, `spostamento_scalare` di `mot.operatori` avvolte IN MEMORIA: dopo l'originale si moltiplica per `z = e^{i pi s f/2}`, che toglie il `conj(z)`; `z` uniforme, l'assert)*; **(iv)** `salta` `CAMM-MATERIA-VUOTO`; **(iv-b)** `salta` `CAMM-FASE-VUOTO`. **(iii) e (v) NON si fanno** *(la carta: (iii) vuole una scelta di Luca; (v) una scena nuova)*.
"""
import contextlib
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import caduta_segno_v2 as CS  # noqa: E402

GRIGLIA = 96
SPETTRO = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1446", "spettro.npz")
E_FONDO = 0.2453383
PIATTA = 1e-6
VARIANTI = (("0", "nessuna ablazione (il caso noto)", (), False), ("i", "la moneta di spin -> l'identita'", ("CAMM-MONETA-SPIN",), False),
            ("ii", "lo zero simmetrico -> lo zero di prima", (), True), ("iv", "il legame col vuoto spento", ("CAMM-MATERIA-VUOTO",), False),
            ("iv-b", "la fase del vuoto spenta", ("CAMM-FASE-VUOTO",), False))
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def tick_abl(z, campo, s, e0, N, salta):
    """### `caduta_segno_v2.tick_var` riga per riga *(`cs_N` False, `segno` 0)* con `salta`."""
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    mot, st, par = z["mot"], z["st"], z["par"]
    campo.spinta(0.5)
    mot.cs = np.full(mot.inc.n, float(s))
    mot.lambda_c = None
    with UO.avvolto(mot, campo, True):
        TK.percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))
    campo.spinta(0.5)


@contextlib.contextmanager
def zero_di_prima(mot):
    """### le quattro voci di `mot.operatori` avvolte: dopo l'originale, `x *= z` *(`z = e^{i pi s f/2}`: toglie il `conj(z)` dello zero simmetrico; uniforme, l'assert)*."""
    import flussi_parziali as FP
    vecchi = {}

    def avvolgi(nome, chiave, per_nodo):
        orig = mot.operatori[nome]
        vecchi[nome] = orig

        def nuovo(st, par, frazione):
            out = orig(st, par, frazione)
            zz = FP.z_nodo(mot, 0.5 * frazione) if per_nodo else FP.z_arco(mot, 0.5 * frazione)
            zz = np.asarray(zz).reshape(-1)
            assert np.all(zz == zz[0]), "z NON uniforme: lo zero non e' una fase globale"
            st[chiave][...] = st[chiave] * zz[0]
            return out
        mot.operatori[nome] = nuovo
    avvolgi("grover", "psi_h", True)
    avvolgi("spostamento_trasporto", "psi_h", False)
    avvolgi("grover_scalare", "phi_h", True)
    avvolgi("spostamento_scalare", "phi_h", False)
    try:
        yield
    finally:
        for k, v in vecchi.items():
            mot.operatori[k] = v


def risposta(salta, zero):
    """### `R[sup]`, `d0[sup]`: le righe di `spettro_gap_v2.main` col tick ablato."""
    import s5_caduta_segno as T4B
    from solitone import toro as TO
    A_IMP = T4B.A_IMP
    MT, PO = TC.moduli()[0], TC.moduli()[5]
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    e0 = float(__import__("s5_coppia_lapse").eps_top_tl4b())
    with TC.scena() as Z:
        mot, st = Z["mot"], Z["st"]
        n, L, s = mot.inc.n, Z["L"], float(Z["s"])
        Z["g_e"] = np.zeros_like(Z["g_e"])
        MT.vuoto_fresco(Z, t0)
        C = PO.campi(Z, rho_c, e)
        base = {x: st[x].copy() for x in Z["chiavi"]}
        A0, E0_, U0 = C.campo.A.copy(), C.campo.E.copy(), mot.geo.U.copy()
        R = np.zeros((n, 12, 12), dtype=complex)
        with (zero_di_prima(mot) if zero else contextlib.nullcontext()):
            for j in range(12):
                us = []
                for f in (1.0, -1.0):
                    for x in Z["chiavi"]:
                        st[x][...] = base[x]
                    p = np.zeros((n, 12), dtype=complex)
                    p[0, j] = f * A_IMP
                    st["psi_h"][...] = p.reshape(st["psi_h"].shape)
                    C.campo.A[...], C.campo.E[...] = A0, E0_
                    mot.geo.U[...] = U0
                    mot.lambda_c = None
                    if salta or zero:
                        tick_abl(Z["z"], C.campo, s, e0, np.ones(n), salta)
                    else:
                        CS.tick_var(Z["z"], C.campo, s, e0, np.ones(n), False, 0)
                    us.append(st["psi_h"].reshape(n, 12).copy())
                R[:, :, j] = (us[0] - us[1]) / (2 * A_IMP)
        d0 = TO.scarti(Z["m1"], Z["m2"], 0.0, 0.0, L)[:, :2]
        for x in Z["chiavi"]:
            st[x][...] = base[x]
        Z["metti"]()
    sup = np.nonzero(np.abs(R).reshape(n, -1).max(axis=1) > 0.0)[0]
    return R[sup], d0[sup]


def main():
    import _presidio
    import s5_caduta_segno as T4B
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "caduta_segno_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "spettro_gap_v2.py"))
    _presidio.avvia(__file__)
    DK = T4B.DK
    print("=" * 130)
    print("[M1658-A] L'ABLAZIONE DELLO SPETTRO (la carta sez. 4): la griglia %d x %d; DK %g; (iii) e (v) NON si fanno (la carta)" % (GRIGLIA, GRIGLIA, DK))
    print("=" * 130)
    A1, A2 = TO.vettori()
    B = 2.0 * np.pi * np.linalg.inv(np.array([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]])).T
    bh = [B[0] / np.linalg.norm(B[0]), B[1] / np.linalg.norm(B[1])]
    kK = (B[0] + B[1]) / 3.0
    rif = {}
    for sig, nome, salta, zero in VARIANTI:
        Rs, ds = risposta(salta, zero)

        def A_di(kv):
            return np.einsum("x,xij->ij", np.exp(-1j * (ds @ kv)), Rs)
        Es = np.zeros((GRIGLIA, GRIGLIA, 12))
        for i in range(GRIGLIA):
            for j in range(GRIGLIA):
                kv = (i * B[0] + j * B[1]) / GRIGLIA
                lam, V = np.linalg.eig(A_di(kv))
                Es[i, j] = -np.angle(lam)
        print("(%s) %s: %d nodi col supporto; |lambda| a Gamma da %.12f a %.12f" % (sig, nome, len(ds), float(np.abs(np.linalg.eigvals(A_di(np.zeros(2)))).min()), float(np.abs(np.linalg.eigvals(A_di(np.zeros(2)))).max())))
        if sig == "0":
            with np.load(SPETTRO) as zf:
                Ef = zf["E"]
            esito("K1 (0) senza ablazione: E(k) = spettro.npz di spettro_gap_v2 AL BIT", Ef.shape == Es.reshape(-1, 12).shape and np.array_equal(Ef, Es.reshape(-1, 12)), "max|dE| %.3e" % (float(np.max(np.abs(Ef - Es.reshape(-1, 12)))) if Ef.shape == Es.reshape(-1, 12).shape else float("nan")))
        So = np.sort(Es.reshape(-1, 12), axis=1)
        righe = []
        for b in range(12):
            lo, hi = float(So[:, b].min()), float(So[:, b].max())
            righe.append("%+.6f..%+.6f%s" % (lo, hi, " PIATTA" if hi - lo < PIATTA else ""))
        print("    le 12 bande ordinate: %s" % "; ".join(righe))
        npiatte = sum(1 for b in range(12) if So[:, b].max() - So[:, b].min() < PIATTA)
        lamG, VG = np.linalg.eig(A_di(np.zeros(2)))
        EG = -np.angle(lamG)
        VG = VG / np.linalg.norm(VG, axis=0)
        lamK, VK = np.linalg.eig(A_di(kK))
        EKs = -np.angle(lamK)
        VK = VK / np.linalg.norm(VK, axis=0)
        if sig == "0":
            o = np.argsort(EG)
            rif["q"] = VG[:, o[-1]]
            jK = [i for i in range(12) if abs(EKs[i] - E_FONDO) < 1e-6]
            Qk, _r = np.linalg.qr(VK[:, jK])
            rif["QK"] = Qk
        ovG = np.abs(VG.conj().T @ rif["q"]) ** 2
        bG = int(np.argmax(ovG))
        q = VG[:, bG]
        ovK = np.sum(np.abs(rif["QK"].conj().T @ VK) ** 2, axis=0)
        bK = int(np.argmax(ovK))
        vK = VK[:, bK]

        def sulla(kv, v):
            w, vr = np.linalg.eig(A_di(kv))
            vr = vr / np.linalg.norm(vr, axis=0)
            b = int(np.argmax(np.abs(vr.conj().T @ v) ** 2))
            return float(-np.angle(w[b]))
        d2G = [(sulla(DK * u, q) - 2.0 * sulla(np.zeros(2), q) + sulla(-DK * u, q)) / DK ** 2 for u in bh]
        d2K = [(sulla(kK + DK * u, vK) - 2.0 * sulla(kK, vK) + sulla(kK - DK * u, vK)) / DK ** 2 for u in bh]
        print("    LA CIMA (a Gamma, la sovrapposizione massima col q senza ablazione %.4f): E %+.7f; d2E/dk2 lungo B0 %+.4e, B1 %+.4e (%s)" % (
            float(ovG[bG]), float(EG[bG]), d2G[0], d2G[1], "MASSA NEGATIVA" if d2G[0] < 0 and d2G[1] < 0 else ("MASSA POSITIVA" if d2G[0] > 0 and d2G[1] > 0 else "MISTA")))
        print("    IL FONDO a K (la sovrapposizione massima col sottospazio del fondo senza ablazione %.4f): E %+.7f; d2E/dk2 lungo B0 %+.4e, B1 %+.4e" % (float(ovK[bK]), float(EKs[bK]), d2K[0], d2K[1]))
        print("    le bande piatte (larghezza < %g): %d" % (PIATTA, npiatte))
        if sig == "0":
            rif["Es"] = Es
        else:
            dsh = (Es.reshape(-1, 12) - rif["Es"].reshape(-1, 12))
            So0 = np.sort(rif["Es"].reshape(-1, 12), axis=1)
            sp = So - So0
            print("    lo spostamento delle bande ordinate rispetto a (0): da %+.6e a %+.6e (uniforme entro %.2e)" % (float(sp.min()), float(sp.max()), float(sp.max() - sp.min())))
        rif[sig] = {"cima": d2G, "piatte": npiatte}
    print("-" * 130)
    print("### K5 (come scritto): «la piatta sparisce con (iii)»: NON GIUDICABILE ((iii) non si fa: la carta)")
    neg = [s_ for s_ in ("i", "ii", "iv", "iv-b") if rif[s_]["cima"][0] < 0 and rif[s_]["cima"][1] < 0]
    print("### K5: la cima a massa negativa resta in %s su %s" % (neg, ["i", "ii", "iv", "iv-b"]))
    print("=" * 130)
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0


if __name__ == "__main__":
    sys.exit(main())
